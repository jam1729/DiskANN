#!/usr/bin/env python3
"""
Run K-Means Tau PQ Byte Allocation search sweep across byte budgets for Scidocs / OpenAI datasets.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List

BYTE_VALUES_DEFAULT = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]


class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()
        self.terminal.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()


def main():
    p = argparse.ArgumentParser(description="Sweep K-Means Tau PQ Search across byte budgets")
    p.add_argument("--dataset", default="scidocs")
    p.add_argument("--model", default="openai_text_large_3")
    p.add_argument("--base_dir", default="/home/jam1729/data/embeddings")
    p.add_argument("--tools_dir", default="/home/jam1729/DiskANN/build/apps/utils")
    p.add_argument("--output_dir", default="/home/jam1729/runs/pq_search_runs")
    p.add_argument("--byte_values", nargs="+", type=int, default=BYTE_VALUES_DEFAULT)
    p.add_argument("--exact_budget", action="store_true", help="Run in exact budget mode instead of weighted")
    p.add_argument("--sampling_rate", type=float, default=0.1)
    p.add_argument("--kmeans_iters", type=int, default=15)
    p.add_argument("--num_buckets", type=int, default=8)
    p.add_argument("--k", type=int, default=100)

    args = p.parse_args()

    dataset_dir = Path(args.base_dir) / args.dataset / args.model
    base_file = dataset_dir / "base.bin"
    query_file = dataset_dir / "query.bin"
    raw_gt_file = dataset_dir / "gt100.bin"
    tools_dir = Path(args.tools_dir)

    for f_path in (base_file, query_file, raw_gt_file):
        if not f_path.exists():
            print(f"Error: dataset file not found: {f_path}")
            sys.exit(1)

    if not tools_dir.exists():
        print(f"Error: tools dir not found: {tools_dir}")
        sys.exit(1)

    mode_name = "exact_budget" if args.exact_budget else "weighted"
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    run_dir = Path(args.output_dir) / args.dataset / args.model / f"kmeans_tau_{mode_name}_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    
    sys.stdout = Logger(run_dir / "stdout")

    script_path = Path(__file__).parent / "kmeans_tau_pq_bucket_search.py"
    python_bin = sys.executable

    results = []

    print("==================================================")
    print(f"Starting K-Means Tau PQ Sweep across budgets: {args.byte_values}")
    print(f"Dataset: {args.dataset} ({args.model})")
    print(f"Mode: {mode_name}")
    print(f"Output dir: {run_dir}")
    print("==================================================")

    for b in args.byte_values:
        work_dir = run_dir / f"bytes_{b}"
        log_json = work_dir / f"trajectory_bytes_{b}.json"
        
        cmd = [
            python_bin,
            str(script_path),
            "--base_file", str(base_file),
            "--query_file", str(query_file),
            "--raw_gt_file", str(raw_gt_file),
            "--work_dir", str(work_dir),
            "--tools_dir", str(tools_dir),
            "--num_buckets", str(args.num_buckets),
            "--total_bytes", str(b),
            "--sampling_rate", str(args.sampling_rate),
            "--kmeans_iters", str(args.kmeans_iters),
            "--k", str(args.k),
            "--log_json", str(log_json),
        ]
        if args.exact_budget:
            cmd.append("--exact_budget")

        print(f"\n---> Running budget B={b} bytes...")
        t0 = time.time()
        proc = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            sys.stdout.write(line)
        proc.wait()
        elapsed = time.time() - t0

        if proc.returncode != 0:
            print(f"[ERROR] Run failed for budget B={b}")
            continue

        if log_json.exists():
            with open(log_json, "r") as f:
                data = json.load(f)
                alloc = data.get("final_allocation")
                recall = data.get("recall_at_k")
                tau = data.get("tau")
                results.append({
                    "total_bytes": b,
                    "final_allocation": alloc,
                    "recall": recall,
                    "tau": tau,
                    "time_seconds": round(elapsed, 2),
                })
                print(f"[SUCCESS] Budget B={b}: Recall@{args.k} = {recall:.6f}, Alloc = {alloc}, Tau = {tau:.4f} ({elapsed:.1f}s)")

    summary_file = run_dir / "sweep_summary.json"
    with open(summary_file, "w") as f:
        json.dump({
            "dataset": args.dataset,
            "model": args.model,
            "mode": mode_name,
            "results": results
        }, f, indent=2)

    print("\n==================================================")
    print("SWEEP COMPLETE!")
    print(f"Summary JSON saved to: {summary_file}")
    print("==================================================")
    print(f"{'Bytes':<8} {'Recall@' + str(args.k):<12} {'Allocation':<30} {'Tau':<10}")
    print("-" * 65)
    for r in results:
        alloc_str = str(r['final_allocation'])
        print(f"{r['total_bytes']:<8} {r['recall']:<12.6f} {alloc_str:<30} {r['tau']:<10.4f}")


if __name__ == "__main__":
    main()
