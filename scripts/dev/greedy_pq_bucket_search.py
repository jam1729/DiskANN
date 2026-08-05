#!/usr/bin/env python3
"""
Greedy search over per-bucket PQ byte allocations to maximize recall of a quantized dataset.

Problem Setting
---------------
We have a continuous float32 base dataset and query file, and a raw ground-truth (GT) file.
We partition the dimensions into N contiguous buckets.
Within each bucket we allocate a number of PQ chunks; each chunk contributes 1 byte.
Using variable-chunk PQ (generate_pq_variable_chunks) we construct chunk offsets.

Search Strategy
---------------
Start from an initial uniform allocation. At each iteration, consider candidates by adding
+increment chunks to one bucket. Train & compress, calculate recall, select best candidate.
Repeat until stopping condition is met.
"""

from __future__ import annotations
import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

from pq_bucket_utils import (
    Config,
    IterRecord,
    CommandError,
    _json_safe,
    save_json_log,
    _read_fbin_header,
    _infer_dimension_and_buckets,
    evaluate_allocation,
    _cleanup_iteration,
    DEFAULT_NUM_BUCKETS,
)


def greedy_search(cfg: Config) -> Dict[str, Any]:
    cfg.work_dir.mkdir(parents=True, exist_ok=True)
    history: List[IterRecord] = []
    current_alloc = [cfg.initial_chunks for _ in range(cfg.num_buckets)]
    best_recall, rec = evaluate_allocation(cfg, current_alloc, tag="init")
    rec.iteration = 0
    rec.improved = True
    history.append(rec)
    if cfg.verbose:
        print(f"Initial allocation {current_alloc} => recall={best_recall:.6f}")

    result = {
        "final_allocation": current_alloc,
        "final_recall": best_recall,
        "history": [dataclasses.asdict(r) for r in history],
    }
    if cfg.log_json:
        save_json_log(cfg.log_json, result)

    prev_iteration_records: List[IterRecord] = [rec]
    candidates: List[Tuple[float, List[int], IterRecord]] = []
    try:
        for it in range(1, cfg.max_iters + 1):
            candidates = []
            for b in range(cfg.num_buckets):
                if current_alloc[b] + cfg.increment > cfg.max_per_bucket:
                    if cfg.verbose:
                        print(f"Iter {it}: Bucket {b} exceeded max_per_bucket")
                    continue
                if (
                    cfg.max_total_bytes is not None
                    and sum(current_alloc) + cfg.increment > cfg.max_total_bytes
                ):
                    if cfg.verbose:
                        print(f"Iter {it}: Total allocation exceeded max_total_bytes")
                    continue
                cand_alloc = current_alloc.copy()
                cand_alloc[b] += cfg.increment
                tag = f"it{it}_b{b}_plus{cfg.increment}"
                try:
                    recall, rec_cand = evaluate_allocation(cfg, cand_alloc, tag=tag)
                except Exception as e:
                    print(f"[WARN] Skipping candidate bucket {b} due to error: {e}")
                    continue
                rec_cand.iteration = it
                candidates.append((recall, cand_alloc, rec_cand))

            if not candidates:
                if cfg.verbose:
                    print("No feasible candidates; stopping.")
                break

            candidates.sort(key=lambda x: (-x[0], sum(x[1]), x[1]))
            best_cand_recall, best_cand_alloc, best_cand_rec = candidates[0]

            is_improvement = best_cand_recall > best_recall + 1e-9
            best_recall = best_cand_recall
            current_alloc = best_cand_alloc
            best_cand_rec.improved = is_improvement
            history.append(best_cand_rec)

            if is_improvement:
                if cfg.verbose:
                    print(
                        f"Iter {it}: improved recall -> {best_recall:.6f} with alloc {current_alloc}"
                    )
            else:
                if cfg.verbose:
                    print(
                        f"Iter {it}: no improvement (best candidate recall={best_cand_recall:.6f}); continuing search."
                    )

            result["final_allocation"] = current_alloc
            result["final_recall"] = best_recall
            result["history"] = [dataclasses.asdict(r) for r in history]
            if cfg.log_json:
                save_json_log(cfg.log_json, result)

            if not cfg.keep_all:
                _cleanup_iteration(
                    prev_iteration_records,
                    preserve_allocation=current_alloc,
                    verbose=cfg.verbose,
                )
            prev_iteration_records = [cand[2] for cand in candidates]
    finally:
        if not cfg.keep_all:
            to_clean = []
            for cand in candidates:
                to_clean.append(cand[2])
            to_clean.extend(prev_iteration_records)
            to_clean.extend(history)
            _cleanup_iteration(
                to_clean, preserve_allocation=current_alloc, verbose=cfg.verbose
            )

    result["final_allocation"] = current_alloc
    result["final_recall"] = best_recall
    result["history"] = [dataclasses.asdict(r) for r in history]
    if cfg.log_json:
        save_json_log(cfg.log_json, result)
    return result


def parse_args(argv: List[str]) -> Config:
    p = argparse.ArgumentParser(description="Greedy PQ bucket byte allocation search")
    p.add_argument("--base_file", required=True)
    p.add_argument("--query_file", required=True)
    p.add_argument(
        "--raw_gt_file", required=True, help="Ground-truth on original base vectors"
    )
    p.add_argument("--work_dir", required=True)
    p.add_argument(
        "--tools_dir",
        required=True,
        help="Directory containing generate_pq_variable_chunks, compute_groundtruth, calculate_recall",
    )
    p.add_argument("--k", type=int, default=100)
    p.add_argument(
        "--num_buckets",
        type=int,
        default=DEFAULT_NUM_BUCKETS,
        help="Number of contiguous buckets to partition the vector dim into",
    )
    p.add_argument("--sampling_rate", type=float, default=0.1)
    p.add_argument("--initial_chunks", type=int, default=8)
    p.add_argument("--increment", type=int, default=8)
    p.add_argument("--max_iters", type=int, default=20)
    p.add_argument("--max_per_bucket", type=int, default=128)
    p.add_argument("--max_total_bytes", type=int, default=None)
    p.add_argument("--keep_all", action="store_true")
    p.add_argument("--pq_prefix_base", default="pq_cfg")
    p.add_argument(
        "--inflate_suffix", default="_pq_compressed.bin_inflated.bin"
    )
    p.add_argument("--log_json")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)
    return Config(
        base_file=Path(args.base_file),
        query_file=Path(args.query_file),
        raw_gt_file=Path(args.raw_gt_file),
        work_dir=Path(args.work_dir),
        tools_dir=Path(args.tools_dir),
        num_buckets=args.num_buckets,
        k=args.k,
        sampling_rate=args.sampling_rate,
        initial_chunks=args.initial_chunks,
        increment=args.increment,
        max_iters=args.max_iters,
        max_per_bucket=args.max_per_bucket,
        max_total_bytes=args.max_total_bytes,
        keep_all=args.keep_all,
        pq_prefix_base=args.pq_prefix_base,
        inflate_suffix=args.inflate_suffix,
        log_json=Path(args.log_json) if args.log_json else None,
        verbose=not args.quiet,
    )


def main(argv: List[str]) -> int:
    cfg = parse_args(argv)
    for path_attr in ("base_file", "query_file", "raw_gt_file", "tools_dir"):
        p = getattr(cfg, path_attr)
        if not p.exists():
            print(f"ERROR: {path_attr} not found: {p}")
            return 1
    try:
        _infer_dimension_and_buckets(cfg)
    except Exception as e:
        print(f"ERROR: failed to infer dimension/buckets: {e}")
        return 1
    try:
        result = greedy_search(cfg)
    except CommandError as e:
        print(f"Execution failed: {e}")
        return 2
    print("\n=== Greedy Search Result ===")
    print("Final allocation:", result["final_allocation"])
    print(f"Final recall@{cfg.k}: {result['final_recall']:.6f}")
    if cfg.log_json:
        print("Log written to:", cfg.log_json)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
