#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import struct
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import numpy as np

# Regex to parse recall from calculate_recall output
RECALL_REGEX = re.compile(r"Avg\. recall@\d+ is ([0-9]*\.?[0-9]+)")

DATASET_MAPPING = {
    "msmarco_500k": "MSmarco",
    "dbpedia_entity_500k": "DBpedia",
    "quora_500k": "Quora",
    "fiqa": "FiQA",
    "scifact": "SciFact",
    "scidocs": "SciDocs"
}

MODEL_MAPPING = {
    "cohere_v4": "Cohere v4",
    "openai_text_large_3": "OpenAI Text Large 3"
}

DATASETS = list(DATASET_MAPPING.keys())
MODELS = list(MODEL_MAPPING.keys())
BUDGETS_MAPPING = {
    "cohere_v4": [32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192],
    "openai_text_large_3": [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
}

def read_fbin_header(path: Path) -> Tuple[int, int]:
    with open(path, 'rb') as f:
        hdr = f.read(8)
        if len(hdr) != 8:
            raise ValueError(f"File too small for header: {path}")
        npts, dim = struct.unpack('<II', hdr)
        return npts, dim

def slice_bin_file(in_path: Path, out_path: Path, target_dim: int):
    """Slices fbin file to target_dim dimensions efficiently."""
    npts, total_dim = read_fbin_header(in_path)
    if target_dim > total_dim:
        raise ValueError(f"target_dim {target_dim} > total_dim {total_dim} in {in_path}")
        
    with open(in_path, 'rb') as f_in:
        f_in.seek(8) # Skip header
        with open(out_path, 'wb') as f_out:
            f_out.write(struct.pack('<II', npts, target_dim))
            
            batch_size = 20000
            row_size = total_dim * 4
            for i in range(0, npts, batch_size):
                cur_batch = min(batch_size, npts - i)
                data = f_in.read(cur_batch * row_size)
                if not data:
                    break
                arr = np.frombuffer(data, dtype=np.float32).reshape(cur_batch, total_dim)
                sliced = arr[:, :target_dim]
                f_out.write(sliced.tobytes())

def run_cmd(cmd: List[str], verbose: bool = True) -> str:
    if verbose:
        print("[CMD]", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\nOutput:\n{proc.stdout}")
    return proc.stdout

def run_truncation_experiment(
    base_file: Path,
    query_file: Path,
    raw_gt_file: Path,
    target_dim: int,
    tools_dir: Path,
    temp_dir: Path,
    k: int = 100,
    verbose: bool = True
) -> float:
    # Set up temp paths
    temp_base = temp_dir / "base_trunc.bin"
    temp_query = temp_dir / "query_trunc.bin"
    temp_gt = temp_dir / "gt100_trunc.bin"
    
    # 1. Slice base and query files
    slice_bin_file(base_file, temp_base, target_dim)
    slice_bin_file(query_file, temp_query, target_dim)
    
    try:
        # 2. Compute groundtruth
        gt_tool = tools_dir / "compute_groundtruth"
        cmd_gt = [
            str(gt_tool),
            "--data_type", "float",
            "--dist_fn", "l2",
            "--base_file", str(temp_base),
            "--query_file", str(temp_query),
            "--gt_file", str(temp_gt),
            "--K", str(k)
        ]
        run_cmd(cmd_gt, verbose=verbose)
        
        # 3. Calculate recall
        recall_tool = tools_dir / "calculate_recall"
        cmd_rec = [
            str(recall_tool),
            str(raw_gt_file),
            str(temp_gt),
            str(k)
        ]
        out_rec = run_cmd(cmd_rec, verbose=verbose)
        
        # Parse recall
        m = RECALL_REGEX.search(out_rec)
        if not m:
            raise RuntimeError("Failed to parse recall from output:\n" + out_rec)
        
        recall = float(m.group(1))
        return recall
        
    finally:
        # Cleanup temp files immediately
        for temp_file in [temp_base, temp_query, temp_gt]:
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

def main():
    p = argparse.ArgumentParser(description="Sweep recall of simply truncated raw float32 embeddings.")
    p.add_argument('--embeddings_dir', default="/home/jam1729/data/embeddings", help="Root directory of embeddings")
    p.add_argument('--diskann_dir', default="/home/jam1729/DiskANN", help="DiskANN home directory")
    p.add_argument('--output_dir', default="/home/jam1729/DiskANN/experiments", help="Directory for final output reports")
    args = p.parse_args()
    
    embeddings_dir = Path(args.embeddings_dir)
    diskann_dir = Path(args.diskann_dir)
    output_dir = Path(args.output_dir)
    tools_dir = diskann_dir / "build/apps/utils"
    
    temp_dir = output_dir / "temp_trunc_run"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    json_output_path = output_dir / "truncation_recall_results.json"
    results = {}
    if json_output_path.exists():
        with open(json_output_path, "r") as f:
            results = json.load(f)
            
    try:
        for dataset in DATASETS:
            if dataset not in results:
                results[dataset] = {}
            for model in MODELS:
                if model not in results[dataset]:
                    results[dataset][model] = {}
                base_file = embeddings_dir / dataset / model / "base.bin"
                query_file = embeddings_dir / dataset / model / "query.bin"
                raw_gt_file = embeddings_dir / dataset / model / "gt100.bin"
                
                if not (base_file.exists() and query_file.exists() and raw_gt_file.exists()):
                    print(f"[WARN] Files missing for dataset {dataset}, model {model}. Skipping.", flush=True)
                    continue
                
                print(f"\n==================================================", flush=True)
                print(f"Starting sweep for Dataset: {dataset}, Model: {model}", flush=True)
                print(f"==================================================", flush=True)
                
                _, total_dim = read_fbin_header(base_file)
                print(f"Dataset total dimension: {total_dim}", flush=True)
                
                model_budgets = BUDGETS_MAPPING[model]
                for budget in model_budgets:
                    if str(budget) in results[dataset][model]:
                        print(f"Skipping budget {budget}B - already computed ({results[dataset][model][str(budget)]:.2f}%)", flush=True)
                        continue
                        
                    target_dim = budget // 4
                    if target_dim > total_dim:
                        print(f"Skipping budget {budget}B (target dimension {target_dim} > total dimension {total_dim})", flush=True)
                        continue
                    
                    print(f"\nEvaluating budget: {budget} Bytes (truncated to {target_dim} dimensions)...", flush=True)
                    try:
                        recall = run_truncation_experiment(
                            base_file=base_file,
                            query_file=query_file,
                            raw_gt_file=raw_gt_file,
                            target_dim=target_dim,
                            tools_dir=tools_dir,
                            temp_dir=temp_dir,
                            k=100,
                            verbose=True
                        )
                        results[dataset][model][str(budget)] = recall
                        print(f"Result for {budget}B ({target_dim}d): Recall@100 = {recall:.6f}", flush=True)
                    except Exception as e:
                        print(f"[ERROR] Failed to run experiment for budget {budget}B: {e}", flush=True)
                        
        # 1. Save JSON output
        json_output_path = output_dir / "truncation_recall_results.json"
        with open(json_output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved machine-readable results to: {json_output_path}", flush=True)
        
        # 2. Generate Markdown table
        md_lines = [
            "# Dimension Truncation Recall Baseline Summary",
            "",
            "This report documents search recall when embeddings are simply truncated (without quantization) to different dimensions corresponding to target bit budgets (in bytes).",
            ""
        ]
        
        for model in MODELS:
            model_name = MODEL_MAPPING[model]
            md_lines.append(f"## {model_name} Model (Recall @ 100)")
            md_lines.append("")
            
            model_budgets = BUDGETS_MAPPING[model]
            
            # Header
            header_cols = ["Dataset"] + [f"{b}B ({b//4}d)" for b in model_budgets]
            md_lines.append("| " + " | ".join(header_cols) + " |")
            md_lines.append("| " + " | ".join([":---"] + [":---" for _ in model_budgets]) + " |")
            
            # Data rows
            for dataset in DATASETS:
                dataset_name = DATASET_MAPPING[dataset]
                row_cols = [dataset_name]
                for budget in model_budgets:
                    rec_val = results.get(dataset, {}).get(model, {}).get(str(budget), None)
                    if rec_val is not None:
                        row_cols.append(f"{rec_val:.2f}%")
                    else:
                        row_cols.append("N/A")
                md_lines.append("| " + " | ".join(row_cols) + " |")
            
            md_lines.append("")
            
        md_output_path = output_dir / "truncation_recall_summary.md"
        with open(md_output_path, "w") as f:
            f.write("\n".join(md_lines))
        print(f"Saved human-readable summary to: {md_output_path}", flush=True)
        
    finally:
        # Cleanup temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
