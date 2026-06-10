#!/usr/bin/env python3
import os
import sys
import json
import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path

# Constants
BYTE_VALUES = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]

def parse_args():
    parser = argparse.ArgumentParser(description="Run complete uniform + variable quantization sweep pipeline")
    parser.add_argument("--dataset", required=True, help="Dataset name (e.g. quora_500k, msmarco_500k, scifact)")
    parser.add_argument("--scheme", required=True, choices=["PQ", "SQ"], help="Quantization scheme (PQ or SQ)")
    parser.add_argument("--model", required=True, choices=["cohere_v4", "openai_text_large_3"], help="Embedding model name")
    parser.add_argument("--allocation_strategy", default="stride", choices=["stride", "frontload"], help="SQ allocation strategy (default: stride)")
    parser.add_argument("--sampling_rate", type=float, default=0.1, help="Sampling rate for quantization sweeps")
    parser.add_argument("--max_total_bytes", type=int, default=384, help="Maximum total bytes limit for greedy search")
    return parser.parse_args()

def run_command(cmd, log_file=None, verbose=True):
    cmd_str = " ".join(cmd)
    if verbose:
        print(f"[CMD] {cmd_str}")
        sys.stdout.flush()
    
    if log_file:
        with open(log_file, "a") as lf:
            lf.write(f"\n--- Running: {cmd_str} at {datetime.now()} ---\n")
            lf.flush()
            res = subprocess.run(cmd, stdout=lf, stderr=lf, text=True)
    else:
        res = subprocess.run(cmd, capture_output=True, text=True)
        
    if res.returncode != 0:
        print(f"[ERROR] Command failed with return code {res.returncode}: {cmd_str}")
        if not log_file:
            print(f"Stdout:\n{res.stdout}\nStderr:\n{res.stderr}")
        sys.stdout.flush()
        raise subprocess.CalledProcessError(res.returncode, cmd)
    return res

def parse_recall(recall_file):
    """Parse output of calculate_recall tool to get float value."""
    with open(recall_file, "r") as f:
        content = f.read().strip()
    # Expecting output format to have a float at the end (e.g., "Avg. recall@100 is 84.7346" or just "84.7346")
    for line in content.split("\n"):
        if "recall" in line.lower():
            parts = line.split()
            for p in parts:
                try:
                    return float(p)
                except ValueError:
                    pass
    # Fallback to last line float parse
    last_line = content.split("\n")[-1]
    for p in last_line.split():
        try:
            return float(p)
        except ValueError:
            pass
    raise ValueError(f"Could not parse recall from content: {content}")

def run_uniform_sweep(args, diskann_dir, base_file, query_file, gt_file, run_dir, pipeline_log):
    print("\n==================================================")
    print("STEP 1: Running Uniform Baseline Sweep...")
    print("==================================================")
    sys.stdout.flush()
    
    uniform_recalls = {}
    
    for target_bytes in BYTE_VALUES:
        print(f"\n--- Uniform Baseline: {target_bytes} Bytes ---")
        sys.stdout.flush()
        
        prefix = os.path.join(run_dir, f"unif_{target_bytes}")
        gt_out = f"{prefix}_gt100"
        recall_log = f"{prefix}_recall.log"
        
        if args.scheme == "PQ":
            compressed = f"{prefix}_pq_compressed.bin"
            inflated = f"{compressed}_inflated.bin"
            pivots = f"{prefix}_pq_pivots.bin"
            
            # 1. Generate PQ
            gen_cmd = [
                os.path.join(diskann_dir, "build/apps/utils/generate_pq"),
                "float", base_file, prefix, str(target_bytes), str(args.sampling_rate), "0"
            ]
            run_command(gen_cmd, pipeline_log)
            
            # 2. Compute GT on reconstructed data
            gt_cmd = [
                os.path.join(diskann_dir, "build/apps/utils/compute_groundtruth"),
                "--data_type", "float",
                "--dist_fn", "l2",
                "--base_file", inflated,
                "--query_file", query_file,
                "--gt_file", gt_out,
                "--K", "100"
            ]
            run_command(gt_cmd, pipeline_log)
            
            # 3. Calculate recall
            rec_cmd = [
                os.path.join(diskann_dir, "build/apps/utils/calculate_recall"),
                gt_file, gt_out, "100"
            ]
            res = run_command(rec_cmd)
            with open(recall_log, "w") as f:
                f.write(res.stdout)
                
            # Parse recall
            recall_val = parse_recall(recall_log)
            uniform_recalls[target_bytes] = recall_val
            print(f"Bytes={target_bytes} (Uniform) - Recall@100: {recall_val:.4f}")
            
            # Cleanup immediately to save space
            for fpath in [compressed, inflated, pivots, gt_out, recall_log]:
                if os.path.exists(fpath):
                    os.remove(fpath)
                    
        elif args.scheme == "SQ":
            compressed = f"{prefix}_sq_compressed.bin"
            inflated = f"{compressed}_inflated.bin"
            cal_file = f"{prefix}_sq_calibration.bin"
            
            # 1. Generate SQ Calibration
            cal_cmd = [
                sys.executable,
                os.path.join(diskann_dir, "experiments/generate_sq_uniform_calibration.py"),
                "--base_file", base_file,
                "--output_cal_file", cal_file,
                "--target_bytes", str(target_bytes),
                "--sampling_rate", str(args.sampling_rate),
                "--seed", "42",
                "--allocation_strategy", args.allocation_strategy
            ]
            run_command(cal_cmd, pipeline_log)
            
            # 2. Generate SQ
            gen_cmd = [
                os.path.join(diskann_dir, "build/apps/utils/generate_sq_variable"),
                base_file, compressed, cal_file
            ]
            run_command(gen_cmd, pipeline_log)
            
            # 3. Reconstruct float32
            recon_cmd = [
                os.path.join(diskann_dir, "build/apps/utils/int8_to_float_scale_variable"),
                compressed, inflated, cal_file
            ]
            run_command(recon_cmd, pipeline_log)
            
            # 4. Compute GT
            gt_cmd = [
                os.path.join(diskann_dir, "build/apps/utils/compute_groundtruth"),
                "--data_type", "float",
                "--dist_fn", "l2",
                "--base_file", inflated,
                "--query_file", query_file,
                "--gt_file", gt_out,
                "--K", "100"
            ]
            run_command(gt_cmd, pipeline_log)
            
            # 5. Calculate Recall
            rec_cmd = [
                os.path.join(diskann_dir, "build/apps/utils/calculate_recall"),
                gt_file, gt_out, "100"
            ]
            res = run_command(rec_cmd)
            with open(recall_log, "w") as f:
                f.write(res.stdout)
                
            # Parse recall
            recall_val = parse_recall(recall_log)
            uniform_recalls[target_bytes] = recall_val
            print(f"Bytes={target_bytes} (Uniform) - Recall@100: {recall_val:.4f}")
            
            # Cleanup immediately
            for fpath in [compressed, inflated, cal_file, gt_out, recall_log]:
                if os.path.exists(fpath):
                    os.remove(fpath)
                    
    return uniform_recalls

def run_variable_sweep(args, diskann_dir, base_file, query_file, gt_file, run_dir, pipeline_log):
    print("\n==================================================")
    print("STEP 2: Running Variable (Greedy) Quantization Search...")
    print("==================================================")
    sys.stdout.flush()
    
    greedy_json = os.path.join(run_dir, "greedy_log.json")
    greedy_stdout = os.path.join(run_dir, "greedy_stdout.log")
    
    if args.scheme == "PQ":
        cmd = [
            sys.executable,
            os.path.join(diskann_dir, "scripts/dev/greedy_pq_bucket_search.py"),
            "--base_file", base_file,
            "--query_file", query_file,
            "--raw_gt_file", gt_file,
            "--work_dir", run_dir,
            "--tools_dir", os.path.join(diskann_dir, "build/apps/utils"),
            "--k", "100",
            "--sampling_rate", str(args.sampling_rate),
            "--num_buckets", "8",
            "--initial_chunks", "8",
            "--increment", "8",
            "--max_per_bucket", "384",
            "--max_total_bytes", str(args.max_total_bytes),
            "--max_iters", "50",
            "--log_json", greedy_json
        ]
    else:  # SQ
        cmd = [
            sys.executable,
            os.path.join(diskann_dir, "scripts/dev/greedy_sq_bucket_search.py"),
            "--base_file", base_file,
            "--query_file", query_file,
            "--raw_gt_file", gt_file,
            "--work_dir", run_dir,
            "--tools_dir", os.path.join(diskann_dir, "build/apps/utils"),
            "--k", "100",
            "--sampling_rate", str(args.sampling_rate),
            "--num_buckets", "8",
            "--initial_chunks", "8",
            "--increment", "8",
            "--max_per_bucket", "384",
            "--max_total_bytes", str(args.max_total_bytes),
            "--max_iters", "50",
            "--allocation_strategy", args.allocation_strategy,
            "--log_json", greedy_json
        ]
        
    print(f"Running search command, logging to: {greedy_stdout}")
    sys.stdout.flush()
    
    with open(greedy_stdout, "w") as out_f:
        res = subprocess.run(cmd, stdout=out_f, stderr=subprocess.STDOUT, text=True)
        
    if res.returncode != 0:
        print(f"[ERROR] Variable search script failed with exit code {res.returncode}")
        sys.stdout.flush()
        raise RuntimeError("Variable greedy search failed.")
        
    print("Variable (Greedy) Search execution complete.")
    sys.stdout.flush()

def aggregate_and_save(args, run_dir, uniform_recalls):
    print("\n==================================================")
    print("STEP 3: Aggregating Results & Generating Outputs...")
    print("==================================================")
    sys.stdout.flush()
    
    greedy_json_path = os.path.join(run_dir, "greedy_log.json")
    if not os.path.exists(greedy_json_path):
        raise FileNotFoundError(f"Could not find greedy search log: {greedy_json_path}")
        
    with open(greedy_json_path, "r") as f:
        greedy_data = json.load(f)
        
    history = greedy_data.get("history", [])
    
    # Organize greedy history by total bytes
    # Since greedy search increments total bytes step-by-step (typically +8 per iteration),
    # we take the best recall for each total byte size evaluated.
    greedy_by_bytes = {}
    for entry in history:
        b_val = entry["bytes_per_vec"]
        rec = entry["recall"]
        alloc = entry["allocation"]
        # If multiple iterations have the same bytes_per_vec, keep the one with the highest recall
        if b_val not in greedy_by_bytes or rec > greedy_by_bytes[b_val]["recall"]:
            greedy_by_bytes[b_val] = {
                "recall": rec,
                "allocation": alloc
            }
            
    summary_results = []
    
    for bytes_val in BYTE_VALUES:
        uni_rec = uniform_recalls.get(bytes_val, 0.0)
        
        # Look up variable/greedy recall for the same byte size
        # If the exact bytes_val is not evaluated in history (e.g. search terminated early),
        # fallback to the closest evaluated size <= bytes_val
        var_rec = 0.0
        var_alloc = []
        
        if bytes_val in greedy_by_bytes:
            var_rec = greedy_by_bytes[bytes_val]["recall"]
            var_alloc = greedy_by_bytes[bytes_val]["allocation"]
        else:
            # Fallback scan
            best_fallback_bytes = -1
            for k in sorted(greedy_by_bytes.keys()):
                if k <= bytes_val:
                    best_fallback_bytes = k
            if best_fallback_bytes != -1:
                var_rec = greedy_by_bytes[best_fallback_bytes]["recall"]
                var_alloc = greedy_by_bytes[best_fallback_bytes]["allocation"]
                
        # Uniform allocation is simply target_bytes/8 for each of the 8 buckets
        uni_alloc = [bytes_val // 8] * 8
        
        # Improvement relative to uniform baseline
        rel_imp = 0.0
        if uni_rec > 0:
            rel_imp = ((var_rec - uni_rec) / uni_rec) * 100.0
            
        summary_results.append({
            "bytes": bytes_val,
            "uniform_alloc": uni_alloc,
            "variable_alloc": var_alloc,
            "uniform_recall": uni_rec,
            "variable_recall": var_rec,
            "improvement": rel_imp
        })
        
    summary = {
        "dataset": args.dataset,
        "scheme": args.scheme,
        "model": args.model,
        "allocation_strategy": args.allocation_strategy if args.scheme == "SQ" else None,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "results": summary_results
    }
    
    summary_json_path = os.path.join(run_dir, "results_summary.json")
    with open(summary_json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved results summary to: {summary_json_path}")
    
    # Generate LaTeX Table
    latex_table = make_latex_table(args.dataset, args.model, args.scheme, summary_results)
    
    summary_tex_path = os.path.join(run_dir, "results_table.tex")
    with open(summary_tex_path, "w") as f:
        f.write(latex_table)
    print(f"Saved LaTeX table to: {summary_tex_path}")
    
    print("\n--------------------------------------------------")
    print("GENERATED LATEX TABLE:")
    print("--------------------------------------------------")
    print(latex_table)
    print("--------------------------------------------------\n")
    sys.stdout.flush()

def make_latex_table(dataset, model, scheme, results):
    model_name = "text-embedding-3-large" if "openai" in model else "cohere-embed-4"
    scheme_name = "Product Quantization (PQ)" if scheme == "PQ" else "Scalar Quantization (SQ)"
    
    latex = []
    latex.append(r"\begin{table*}[htbp]")
    latex.append(r"    \centering")
    latex.append(f"    \\caption{{Comparison of Uniform vs. Variable (Greedy) Bit Allocation for {scheme_name} on {dataset} using \\texttt{{{model_name}}} (Truncated to 500k).}}")
    latex.append(f"    \\label{{tab:{dataset}_{model}_{scheme.lower()}_alloc}}")
    latex.append(r"    \resizebox{\textwidth}{!}{")
    latex.append(r"    \begin{tabular}{cccccc}")
    latex.append(r"        \toprule")
    latex.append(r"        & \multicolumn{2}{c}{\textbf{Allocation Strategy (Bytes per Block)}} & \multicolumn{3}{c}{\textbf{Recall (\%)}} \\")
    latex.append(r"        \cmidrule(lr){2-3} \cmidrule(lr){4-6}")
    latex.append(r"        \textbf{Total Bytes} & \textbf{Uniform Baseline} & \textbf{Variable (Greedy)} & \textbf{Uniform} & \textbf{Variable} & \textbf{Improvement} \\")
    latex.append(r"        \midrule")
    
    # Calculate maximum relative improvement to bold it
    max_imp = -100.0
    for r in results:
        if r["uniform_recall"] > 0:
            imp = ((r["variable_recall"] - r["uniform_recall"]) / r["uniform_recall"]) * 100.0
            if imp > max_imp:
                max_imp = imp
                
    for r in results:
        bytes_val = r["bytes"]
        uni_alloc = str(r["uniform_alloc"])
        var_alloc = str(r["variable_alloc"])
        uni_rec = f"{r['uniform_recall']:.2f}"
        var_rec = f"{r['variable_recall']:.2f}"
        
        if r["uniform_recall"] > 0:
            imp_val = ((r["variable_recall"] - r["uniform_recall"]) / r["uniform_recall"]) * 100.0
            imp_str = f"+{imp_val:.2f}\\%" if imp_val >= 0 else f"{imp_val:.2f}\\%"
            if abs(imp_val - max_imp) < 1e-5:
                imp_str = f"\\textbf{{{imp_str}}}"
        else:
            imp_str = "0.00\\%"
            
        latex.append(f"        {bytes_val:<4} & {uni_alloc:<30} & {var_alloc:<34} & {uni_rec:<5} & {var_rec:<5} & {imp_str} \\\\")
        
    latex.append(r"        \bottomrule")
    latex.append(r"    \end{tabular}")
    latex.append(r"    }")
    latex.append(r"\end{table*}")
    return "\n".join(latex)

def clean_final_binaries(run_dir):
    """Clean up any leftover compressed or inflated binaries from the runs dir."""
    print("Performing final cleanup of large intermediate binaries...")
    count = 0
    for ext in ["*_inflated.bin", "*.bin"]:
        # Match only files that are temporary config artifacts
        for p in Path(run_dir).glob(ext):
            # Do not delete results_summary.json, log.json, table.tex, etc.
            # Do not delete sq_calibration.bin files if they are needed, wait, calibrations are tiny (~KBs), but clean them to be safe
            if p.name not in ["base.bin", "query.bin", "gt100.bin"]:
                try:
                    p.unlink()
                    count += 1
                except Exception:
                    pass
    print(f"Cleaned up {count} binary/index files from the runs directory.")
    sys.stdout.flush()

def main():
    args = parse_args()
    
    diskann_dir = "/home/jam1729/DiskANN"
    embeddings_dir = "/home/jam1729/data/embeddings"
    
    # Target files
    base_file = os.path.join(embeddings_dir, args.dataset, args.model, "base.bin")
    query_file = os.path.join(embeddings_dir, args.dataset, args.model, "query.bin")
    gt_file = os.path.join(embeddings_dir, args.dataset, args.model, "gt100.bin")
    
    for path in [base_file, query_file, gt_file]:
        if not os.path.exists(path):
            print(f"[ERROR] Required file not found: {path}")
            sys.exit(1)
            
    # Setup Run Dir
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(
        "/home/jam1729/runs",
        f"{args.scheme.lower()}_search_runs",
        args.dataset,
        args.model,
        f"run_{timestamp}"
    )
    os.makedirs(run_dir, exist_ok=True)
    
    pipeline_log = os.path.join(run_dir, "pipeline_execution.log")
    
    print(f"\n==================================================")
    print(f"STARTING SWEEP PIPELINE FOR:")
    print(f"Dataset:   {args.dataset}")
    print(f"Scheme:    {args.scheme}")
    print(f"Model:     {args.model}")
    print(f"Run Dir:   {run_dir}")
    print(f"==================================================")
    sys.stdout.flush()
    
    with open(pipeline_log, "w") as f:
        f.write(f"Pipeline Sweep Started: {datetime.now()}\n")
        
    try:
        # Step 1: Run Uniform baseline
        uniform_recalls = run_uniform_sweep(args, diskann_dir, base_file, query_file, gt_file, run_dir, pipeline_log)
        
        # Step 2: Run Variable sweep
        run_variable_sweep(args, diskann_dir, base_file, query_file, gt_file, run_dir, pipeline_log)
        
        # Step 3: Aggregate results
        aggregate_and_save(args, run_dir, uniform_recalls)
        
        # Step 4: Cleanup final remaining binaries
        clean_final_binaries(run_dir)
        
        print(f"\nSweep pipeline completed successfully! Outputs are logged to {run_dir}\n")
        
    except Exception as e:
        print(f"\n[FATAL ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
