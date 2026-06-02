#!/usr/bin/env python3
"""
Greedy search over per-bucket Scalar Quantization (SQ) byte allocations to maximize recall.

Problem Setting
---------------
We have a continuous float32 base dataset and query file, and a raw ground-truth (GT) file.
We partition the D dimensions into B contiguous buckets.
Within each bucket, we allocate a target byte budget.
Using balanced dimension calibration (using allowed bit widths {0, 2, 4, 8}), we distribute
the allocated bits per bucket as evenly as possible across the dimensions in that bucket.
We simulate variable SQ via precision truncation inside a standard int8_t container.

Search Strategy
---------------
Start from an initial uniform byte allocation (default: initial_chunks bytes per bucket).
At each iteration, consider upgrading one bucket by increment bytes.
Quantize, inflate, and compute quantized search recall for each candidate.
Select the candidate with the highest recall improvement.
Repeat until no candidate improves recall or we hit constraints (max iterations, max_per_bucket, max_total_bytes).

External Tools (must be compiled):
  generate_sq_variable
  int8_to_float_scale_variable
  compute_groundtruth
  calculate_recall
"""
from __future__ import annotations
import argparse
import dataclasses
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any
import numpy as np

RECALL_REGEX = re.compile(r"Avg\. recall@\d+ is ([0-9]*\.?[0-9]+)")

@dataclasses.dataclass
class Config:
    base_file: Path
    query_file: Path
    raw_gt_file: Path
    work_dir: Path
    tools_dir: Path
    dim: int = -1
    num_buckets: int = 8
    bucket_sizes: List[int] = dataclasses.field(default_factory=list)
    k: int = 100
    sampling_rate: float = 0.1
    initial_chunks: int = 8
    increment: int = 8
    max_iters: int = 20
    max_per_bucket: int = 192
    max_total_bytes: int | None = None
    keep_all: bool = False
    log_json: Path | None = None
    verbose: bool = True
    seed: int = 42
    allocation_strategy: str = "stride"

@dataclasses.dataclass
class IterRecord:
    iteration: int
    allocation: List[int]
    recall: float
    avg_bytes_per_vec: float
    improved: bool
    tag: str
    artifacts: List[Path] = dataclasses.field(default_factory=list)

class CommandError(RuntimeError):
    pass

def run_cmd(cmd: List[str], verbose: bool = True) -> str:
    if verbose:
        print("[CMD]", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    if proc.returncode != 0:
        raise CommandError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\nOutput:\n{proc.stdout}")
    return proc.stdout

def calibrate_dimensions(cfg: Config) -> Tuple[List[float], List[float]]:
    """Read base file header and sample vectors to compute dynamic range per dimension."""
    if cfg.verbose:
        print(f"Calibrating dimension ranges using {cfg.sampling_rate * 100:.1f}% of base dataset...", flush=True)
    
    with open(cfg.base_file, 'rb') as f:
        npts = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        dim = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        assert dim == cfg.dim, f"Dimension mismatch between header ({dim}) and expected ({cfg.dim})"
        
        sample_npts = max(1, int(npts * cfg.sampling_rate))
        
        # True uniform random sampling
        indices = np.random.choice(npts, size=sample_npts, replace=False)
        indices.sort() # Sorted access ensures linear, high-speed disk seek
        
        data = np.empty((sample_npts, dim), dtype=np.float32)
        for i, idx in enumerate(indices):
            f.seek(8 + idx * dim * 4)
            data[i] = np.fromfile(f, dtype=np.float32, count=dim)
            
        mins = np.min(data, axis=0)
        maxes = np.max(data, axis=0)
        
        bias = mins.tolist()
        scale = (maxes - mins).tolist()
        
        # Avoid division by zero
        for d in range(cfg.dim):
            if scale[d] <= 1e-9:
                scale[d] = 1.0
                
        return bias, scale

def save_calibration(bias: List[float], scale: List[float], bit_widths: List[int], out_path: Path):
    ndims = len(bias)
    with open(out_path, 'wb') as f:
        f.write(struct.pack('<I', ndims))
        f.write(struct.pack(f'<{ndims}f', *bias))
        f.write(struct.pack(f'<{ndims}f', *scale))
        f.write(struct.pack(f'<{ndims}B', *bit_widths))

def build_dim_bit_widths(cfg: Config, allocation: List[int]) -> List[int]:
    """Map bucket-level byte allocations to dimension-level bit widths using balanced calibration."""
    def select_k_indices(d_size: int, k_val: int) -> list[int]:
        if k_val <= 0:
            return []
        if k_val >= d_size:
            return list(range(d_size))
        idx_list = []
        acc = 0
        for i in range(d_size):
            acc += k_val
            if acc >= d_size:
                idx_list.append(i)
                acc -= d_size
        return idx_list

    dim_widths = []
    for b_idx, b_size in enumerate(cfg.bucket_sizes):
        b_bytes = allocation[b_idx]
        total_bits_needed = b_bytes * 8
        max_bits_possible = b_size * 8
        if total_bits_needed > max_bits_possible:
            total_bits_needed = max_bits_possible
            
        b_widths = [0] * b_size
        if cfg.allocation_strategy == 'stride':
            if total_bits_needed <= b_size * 2:
                n2 = total_bits_needed // 2
                indices = select_k_indices(b_size, n2)
                for idx in indices:
                    b_widths[idx] = 2
            elif total_bits_needed <= b_size * 4:
                n4 = (total_bits_needed - 2 * b_size) // 2
                indices = select_k_indices(b_size, n4)
                indices_set = set(indices)
                for i in range(b_size):
                    b_widths[i] = 4 if i in indices_set else 2
            else:
                n8 = (total_bits_needed - 4 * b_size) // 4
                indices = select_k_indices(b_size, n8)
                indices_set = set(indices)
                for i in range(b_size):
                    b_widths[i] = 8 if i in indices_set else 4
        else:
            # Default: front_load
            if total_bits_needed <= b_size * 2:
                # Levels: 0 and 2.
                n2 = total_bits_needed // 2
                for i in range(min(n2, b_size)):
                    b_widths[i] = 2
            elif total_bits_needed <= b_size * 4:
                # Levels: 2 and 4.
                n4 = (total_bits_needed - 2 * b_size) // 2
                n4 = max(0, min(n4, b_size))
                for i in range(b_size):
                    b_widths[i] = 4 if i < n4 else 2
            else:
                # Levels: 4 and 8.
                n8 = (total_bits_needed - 4 * b_size) // 4
                n8 = max(0, min(n8, b_size))
                for i in range(b_size):
                    b_widths[i] = 8 if i < n8 else 4
                    
        dim_widths.extend(b_widths)
        
    assert len(dim_widths) == cfg.dim
    return dim_widths

def train_and_quantize(cfg: Config, bias: List[float], scale: List[float], allocation: List[int], tag: str) -> Tuple[Path, Path, Path]:
    """Runs C++ quantization and inflation utilities for a layout allocation."""
    dim_widths = build_dim_bit_widths(cfg, allocation)
    
    cal_file = cfg.work_dir / f"cal_{tag}.bin"
    save_calibration(bias, scale, dim_widths, cal_file)
    
    quant_out = cfg.work_dir / f"quant_{tag}.bin"
    quant_tool = cfg.tools_dir / "generate_sq_variable"
    quant_cmd = [str(quant_tool), str(cfg.base_file), str(quant_out), str(cal_file)]
    run_cmd(quant_cmd, verbose=cfg.verbose)
    
    inflated_out = cfg.work_dir / f"inflated_{tag}.bin"
    dequant_tool = cfg.tools_dir / "int8_to_float_scale_variable"
    dequant_cmd = [str(dequant_tool), str(quant_out), str(inflated_out), str(cal_file)]
    run_cmd(dequant_cmd, verbose=cfg.verbose)
    
    return cal_file, quant_out, inflated_out

def compute_recall(cfg: Config, inflated_file: Path, tag: str) -> Tuple[float, Path]:
    """Computes recall of the inflated continuous float dataset vs original raw ground truth."""
    gt_out = cfg.work_dir / f"gt_{tag}.bin"
    gt_tool = cfg.tools_dir / "compute_groundtruth"
    gt_cmd = [str(gt_tool), "--data_type", "float", "--dist_fn", "l2", "--base_file", str(inflated_file),
              "--query_file", str(cfg.query_file), "--gt_file", str(gt_out), "--K", str(cfg.k)]
    run_cmd(gt_cmd, verbose=cfg.verbose)
    
    recall_tool = cfg.tools_dir / "calculate_recall"
    recall_cmd = [str(recall_tool), str(cfg.raw_gt_file), str(gt_out), str(cfg.k)]
    out = run_cmd(recall_cmd, verbose=cfg.verbose)
    
    m = RECALL_REGEX.search(out)
    if not m:
        raise RuntimeError(f"Failed to parse recall from output:\n{out}")
        
    return float(m.group(1)), gt_out

def evaluate_allocation(cfg: Config, bias: List[float], scale: List[float], allocation: List[int], tag: str) -> Tuple[float, IterRecord]:
    cal_file, quant_out, inflated_out = train_and_quantize(cfg, bias, scale, allocation, tag)
    recall, gt_out = compute_recall(cfg, inflated_out, tag)
    
    avg_bytes = sum(allocation)
    
    if cfg.verbose:
        print(f"SQ_GREEDY_EVAL tag={tag} alloc={allocation} bytes={avg_bytes} recall={recall:.6f}", flush=True)
        
    artifacts = [cal_file, quant_out, inflated_out, gt_out]
    return recall, IterRecord(
        iteration=-1,
        allocation=allocation.copy(),
        recall=recall,
        avg_bytes_per_vec=float(avg_bytes),
        improved=False,
        tag=tag,
        artifacts=artifacts
    )

def greedy_search(cfg: Config, bias: List[float], scale: List[float]) -> Dict[str, Any]:
    cfg.work_dir.mkdir(parents=True, exist_ok=True)
    history: List[IterRecord] = []
    
    # Initialize with uniform allocation (initial_chunks bytes per bucket)
    current_alloc = [cfg.initial_chunks for _ in range(cfg.num_buckets)]
    best_recall, rec = evaluate_allocation(cfg, bias, scale, current_alloc, tag="init")
    rec.iteration = 0
    rec.improved = True
    history.append(rec)
    
    if cfg.verbose:
        print(f"\nInitial uniform allocation {current_alloc} ({rec.avg_bytes_per_vec:.1f} bytes) => recall={best_recall:.6f}\n")
        
    prev_iteration_records: List[IterRecord] = [rec]
    
    for it in range(1, cfg.max_iters + 1):
        candidates: List[Tuple[float, List[int], IterRecord]] = []
        
        for b in range(cfg.num_buckets):
            if current_alloc[b] + cfg.increment > cfg.max_per_bucket:
                continue
            if cfg.max_total_bytes is not None and sum(current_alloc) + cfg.increment > cfg.max_total_bytes:
                continue
                
            cand_alloc = current_alloc.copy()
            cand_alloc[b] += cfg.increment
            tag = f"it{it}_b{b}_plus{cfg.increment}"
            
            try:
                recall, rec_cand = evaluate_allocation(cfg, bias, scale, cand_alloc, tag=tag)
                rec_cand.iteration = it
                candidates.append((recall, cand_alloc, rec_cand))
            except Exception as e:
                print(f"[WARN] Skipping candidate bucket {b} due to error: {e}")
                continue
                
        if not candidates:
            if cfg.verbose:
                print("All buckets at maximum precision or budget constraint met. Stopping search.")
            break
            
        # Select candidate with best recall (tie-breaker: fewer bytes, then lexicographically)
        candidates.sort(key=lambda x: (-x[0], x[2].avg_bytes_per_vec, x[1]))
        best_cand_recall, best_cand_alloc, best_cand_rec = candidates[0]
        
        if best_cand_recall > best_recall + 1e-9:
            best_recall = best_cand_recall
            current_alloc = best_cand_alloc
            best_cand_rec.improved = True
            history.append(best_cand_rec)
            
            if cfg.verbose:
                print(f"\n[ITER {it}] Upgrade SUCCESS -> New recall={best_recall:.6f} with alloc {current_alloc} ({best_cand_rec.avg_bytes_per_vec:.1f} bytes)\n")
        else:
            best_cand_rec.improved = False
            history.append(best_cand_rec)
            if cfg.verbose:
                print(f"\n[ITER {it}] No candidate improved recall (best candidate recall={best_cand_recall:.6f}). Stopping search.\n")
            if not cfg.keep_all:
                _cleanup_iteration(prev_iteration_records, preserve_allocation=current_alloc, verbose=cfg.verbose)
            break
            
        if not cfg.keep_all:
            _cleanup_iteration(prev_iteration_records, preserve_allocation=current_alloc, verbose=cfg.verbose)
        prev_iteration_records = [cand[2] for cand in candidates]
        
    # Serialize results
    result = {
        "final_allocation": current_alloc,
        "final_recall": best_recall,
        "history": [dataclasses.asdict(r) for r in history]
    }
    
    if cfg.log_json:
        with open(cfg.log_json, 'w') as f:
            json.dump(result, f, default=str, indent=2)
            
    return result

def _cleanup_iteration(records: List[IterRecord], preserve_allocation: List[int], verbose: bool):
    """Deletes temporary files of a completed iteration except the current best config."""
    for rec in records:
        if rec.allocation == preserve_allocation:
            continue
        for path in rec.artifacts:
            try:
                if path.exists():
                    path.unlink()
            except Exception:
                pass
    if verbose:
        print("[CLEANUP] Recycled temporary binary files for non-optimal candidates.")

def _read_fbin_header(path: Path) -> Tuple[int, int]:
    """Read DiskANN float32 binary header: returns (npts, dim)."""
    with open(path, 'rb') as f:
        hdr = f.read(8)
        if len(hdr) != 8:
            raise ValueError(f"File too small for header: {path}")
        npts, dim = struct.unpack('<II', hdr)
        if npts == 0 or dim == 0:
            raise ValueError(f"Invalid header values in {path}: npts={npts} dim={dim}")
        return npts, dim

def _infer_dimension_and_buckets(cfg: Config):
    """Infers dim from files and creates uniform contiguous bucket bounds."""
    _, dim_base = _read_fbin_header(cfg.base_file)
    _, dim_query = _read_fbin_header(cfg.query_file)
    if dim_base != dim_query:
        raise ValueError(f"Base/query dim mismatch: {dim_base} vs {dim_query}")
    cfg.dim = dim_base
    
    # Partition dimensions evenly
    base_bucket = cfg.dim // cfg.num_buckets
    rem = cfg.dim % cfg.num_buckets
    cfg.bucket_sizes = [base_bucket + (1 if i < rem else 0) for i in range(cfg.num_buckets)]
    if cfg.verbose:
        print(f"Configuration: dimension={cfg.dim}, buckets={cfg.num_buckets}, bucket_sizes={cfg.bucket_sizes}")

def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Greedy Variable SQ layout search by bytes")
    parser.add_argument('--base_file', required=True)
    parser.add_argument('--query_file', required=True)
    parser.add_argument('--raw_gt_file', required=True)
    parser.add_argument('--work_dir', required=True)
    parser.add_argument('--tools_dir', required=True)
    parser.add_argument('--k', type=int, default=100)
    parser.add_argument('--num_buckets', type=int, default=8)
    parser.add_argument('--sampling_rate', type=float, default=0.1)
    parser.add_argument('--initial_chunks', type=int, default=8)
    parser.add_argument('--increment', type=int, default=8)
    parser.add_argument('--max_iters', type=int, default=20)
    parser.add_argument('--max_per_bucket', type=int, default=192)
    parser.add_argument('--max_total_bytes', type=int, default=None)
    parser.add_argument('--keep_all', action='store_true')
    parser.add_argument('--log_json')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--seed', type=int, default=42, help='Seed for random number generator')
    parser.add_argument('--allocation_strategy', choices=['front_load', 'stride'], default='stride',
                        help='Strategy to distribute bits across dimensions')
    
    args = parser.parse_args(argv)
    
    # Set seed for reproducibility
    np.random.seed(args.seed)
    
    cfg = Config(
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
        log_json=Path(args.log_json) if args.log_json else None,
        verbose=not args.quiet,
        seed=args.seed,
        allocation_strategy=args.allocation_strategy
    )
    
    # Check paths exist
    for p_name, path in [('base_file', cfg.base_file), ('query_file', cfg.query_file), 
                         ('raw_gt_file', cfg.raw_gt_file), ('tools_dir', cfg.tools_dir)]:
        if not path.exists():
            print(f"ERROR: {p_name} not found: {path}")
            return 1
            
    # Infer D and partition buckets first, then calibrate dimension ranges
    try:
        _infer_dimension_and_buckets(cfg)
        bias, scale = calibrate_dimensions(cfg)
    except Exception as e:
        print(f"ERROR during initialization/calibration: {e}")
        return 1
        
    try:
        result = greedy_search(cfg, bias, scale)
    except CommandError as e:
        print(f"Execution error running C++ tools: {e}")
        return 2
        
    print("\n=== SQ Greedy Search Results ===")
    print("Final Optimal Allocation Vector:", result['final_allocation'])
    print(f"Final Recall@{cfg.k}: {result['final_recall']:.6f}")
    if cfg.log_json:
        print("Detailed trajectory logged to:", cfg.log_json)
        
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
