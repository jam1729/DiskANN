#!/usr/bin/env python3
import os
import sys
import time
import argparse
import subprocess
from datetime import datetime

MASTER_LOG_PATH = "/home/jam1729/runs/master_orchestrator.log"

def parse_args():
    parser = argparse.ArgumentParser(description="Master orchestrator to run quantization sweeps in parallel tmux sessions")
    parser.add_argument("--dataset", required=True, help="Dataset name (e.g. scifact, quora_500k, msmarco_500k)")
    parser.add_argument("--schemes", default="PQ,SQ", help="Comma-separated schemes (default: PQ,SQ)")
    parser.add_argument("--models", default="cohere_v4,openai_text_large_3", help="Comma-separated models (default: cohere_v4,openai_text_large_3)")
    parser.add_argument("--parallel", type=int, default=1, help="Max parallel runs (default: 1)")
    return parser.parse_args()

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    print(formatted_msg)
    sys.stdout.flush()
    
    # Ensure runs directory exists
    os.makedirs(os.path.dirname(MASTER_LOG_PATH), exist_ok=True)
    with open(MASTER_LOG_PATH, "a") as f:
        f.write(formatted_msg + "\n")

def check_tmux_session_exists(session_name):
    cmd = ["tmux", "has-session", "-t", session_name]
    res = subprocess.run(cmd, capture_output=True)
    return res.returncode == 0

def start_tmux_session(session_name, cmd):
    # -d starts the session in detached mode
    tmux_cmd = ["tmux", "new-session", "-d", "-s", session_name, cmd]
    res = subprocess.run(tmux_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to start tmux session {session_name}: {res.stderr}")

def get_session_name(scheme, dataset, model):
    # Tmux session names cannot contain periods. Clean up dataset and model.
    ds_clean = dataset.replace(".", "_")
    model_clean = model.replace(".", "_")
    return f"sweep_{scheme.lower()}_{ds_clean}_{model_clean}"

def print_queue_status(running, pending, completed):
    log("\n" + "="*60)
    log("CURRENT RUN STATUS:")
    log(f"Running:   {len(running)} / {args_parallel_limit}")
    log(f"Pending:   {len(pending)}")
    log(f"Completed: {len(completed)}")
    log("="*60)
    
    if running:
        log("ACTIVE RUNS:")
        for job, session in running.items():
            log(f"  * {job[0]} - {job[1]} (tmux: {session})")
            
    if pending:
        log("PENDING RUNS:")
        for job in pending:
            log(f"  - {job[0]} - {job[1]}")
            
    log("="*60 + "\n")

args_parallel_limit = 1

def main():
    global args_parallel_limit
    args = parse_args()
    args_parallel_limit = args.parallel
    
    schemes = [s.strip() for s in args.schemes.split(",") if s.strip()]
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    
    # Create the job queue of (scheme, model)
    pending_jobs = []
    for scheme in schemes:
        for model in models:
            pending_jobs.append((scheme, model))
            
    running_jobs = {} # (scheme, model) -> session_name
    completed_jobs = []
    
    log("==================================================")
    log(f"Master Orchestrator Started for Dataset: {args.dataset}")
    log(f"Queue Size: {len(pending_jobs)} combinations")
    log(f"Max Parallelism Limit: {args.parallel}")
    log(f"Log Streaming Path: {MASTER_LOG_PATH}")
    log("==================================================")
    
    diskann_dir = "/home/jam1729/DiskANN"
    pipeline_script = os.path.join(diskann_dir, "experiments/scripts/run_sweep_pipeline.py")
    
    # Check if frontail is running, if not suggest starting it
    log("Tip: You can monitor progress remotely via frontail using:")
    log(f"  frontail -n 100000 -p 9001 {MASTER_LOG_PATH}")
    
    print_queue_status(running_jobs, pending_jobs, completed_jobs)
    
    try:
        while pending_jobs or running_jobs:
            # 1. Check active jobs and harvest finished ones
            finished_jobs = []
            for job, session in running_jobs.items():
                if not check_tmux_session_exists(session):
                    finished_jobs.append(job)
                    
            for job in finished_jobs:
                session = running_jobs.pop(job)
                completed_jobs.append(job)
                log(f"SUCCESS: Job {job[0]} - {job[1]} finished (tmux session {session} closed).")
                print_queue_status(running_jobs, pending_jobs, completed_jobs)
                
            # 2. Schedule pending jobs if slots are available
            while len(running_jobs) < args.parallel and pending_jobs:
                job = pending_jobs.pop(0)
                scheme, model = job
                session_name = get_session_name(scheme, args.dataset, model)
                
                # Make sure a session with the same name isn't already running
                if check_tmux_session_exists(session_name):
                    log(f"[WARNING] Tmux session '{session_name}' is already running. Killing it to start fresh...")
                    subprocess.run(["tmux", "kill-session", "-t", session_name])
                    
                # Build command to execute inside tmux
                cmd = f"{sys.executable} {pipeline_script} --dataset {args.dataset} --scheme {scheme} --model {model}"
                
                log(f"STARTING: Job {scheme} - {model} inside tmux session '{session_name}'")
                start_tmux_session(session_name, cmd)
                
                running_jobs[job] = session_name
                print_queue_status(running_jobs, pending_jobs, completed_jobs)
                
            # Sleep before next polling cycle
            time.sleep(10)
            
        log("==================================================")
        log("ALL SCHEDULER SWEEP JOBS COMPLETED! 🎉")
        log("==================================================")
        
    except KeyboardInterrupt:
        log("\nOrchestrator interrupted by user. Active sessions are left running in tmux.")
        sys.exit(130)

if __name__ == "__main__":
    main()
