#!/usr/bin/env python3
"""
Orchestrates and compares Global OPQ, Uniform Block-OPQ, and Variable Block-OPQ
under Matryoshka Representation Learning (MRL) constraints for DiskANN.

We enforce block-diagonal constraints on the rotation matrix to prevent cross-bucket dimension leakage,
allowing zero-leakage search-time truncation while using DiskANN's built-in query rotation natively.
"""

from __future__ import annotations
import argparse
import dataclasses
import json
import os
import re
import shutil
import subprocess
import sys
import struct
import time
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
    max_iters: int = 50
    max_per_bucket: int = 384
    max_total_bytes: int = 384
    keep_all: bool = False
    pq_prefix_base: str = 'opq_cfg'
    verbose: bool = True
    opq_cache_dir: Path | None = None
    clear_opq_cache: bool = False

@dataclasses.dataclass
class IterRecord:
    iteration: int
    allocation: List[int]
    recall: float
    bytes_per_vec: int
    prefix: str
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

def read_fbin_header(path: Path) -> Tuple[int, int]:
    with open(path, 'rb') as f:
        hdr = f.read(8)
        if len(hdr) != 8:
            raise ValueError(f"File too small for header: {path}")
        npts, dim = struct.unpack('<II', hdr)
        return npts, dim

def write_fbin_header(f, npts: int, dim: int):
    f.write(struct.pack('<II', npts, dim))

def slice_bin_file(in_path: Path, out_paths: List[Path], bucket_sizes: List[int], verbose: bool = True):
    """Slices a standard float32 bin file into bucket slice files memory-efficiently."""
    npts, total_dim = read_fbin_header(in_path)
    if sum(bucket_sizes) != total_dim:
        raise ValueError(f"Bucket sizes sum ({sum(bucket_sizes)}) != total dim ({total_dim})")
    
    if verbose:
        print(f"Slicing {in_path} (npts={npts}, dim={total_dim}) into {len(out_paths)} buckets...", flush=True)

    # Open output file handles
    writers = []
    for path, b_dim in zip(out_paths, bucket_sizes):
        f = open(path, 'wb')
        write_fbin_header(f, npts, b_dim)
        writers.append(f)

    # Stream in chunks of vectors to conserve memory
    chunk_size = 10000
    with open(in_path, 'rb') as f_in:
        f_in.seek(8)  # skip header
        for i in range(0, npts, chunk_size):
            actual_chunk = min(chunk_size, npts - i)
            # Just read actual_chunk * total_dim floats
            float_count = actual_chunk * total_dim
            data = f_in.read(float_count * 4)
            if not data:
                break
            
            actual_read_pts = len(data) // (total_dim * 4)
            if actual_read_pts == 0:
                break

            # Reshape into a 2D float array
            arr = np.frombuffer(data, dtype=np.float32).reshape(actual_read_pts, total_dim)

            # Write slices
            start_col = 0
            for w, b_dim in zip(writers, bucket_sizes):
                slice_arr = arr[:, start_col : start_col + b_dim]
                w.write(slice_arr.tobytes())
                start_col += b_dim

    for w in writers:
        w.close()

    if verbose:
        print("Slicing completed successfully.", flush=True)

# Helper functions for DiskANN save/load bin compatibility
def load_bin_numpy_float(path: Path, offset: int = 0) -> Tuple[np.ndarray, int, int]:
    with open(path, 'rb') as f:
        f.seek(offset)
        nr, nc = struct.unpack('<ii', f.read(8))
        bytes_to_read = nr * nc * 4
        data = np.frombuffer(f.read(bytes_to_read), dtype=np.float32)
        return data.reshape(nr, nc), nr, nc

def load_bin_numpy_uint32(path: Path, offset: int = 0) -> Tuple[np.ndarray, int, int]:
    with open(path, 'rb') as f:
        f.seek(offset)
        nr, nc = struct.unpack('<ii', f.read(8))
        bytes_to_read = nr * nc * 4
        data = np.frombuffer(f.read(bytes_to_read), dtype=np.uint32)
        return data.reshape(nr, nc), nr, nc

def save_bin_numpy(path: Path, arr: np.ndarray, offset: int = 0, mode: str = 'wb') -> int:
    nr, nc = arr.shape[0], arr.shape[1] if len(arr.shape) > 1 else 1
    bytes_written = 8 + arr.nbytes
    with open(path, 'r+b' if offset > 0 else mode) as f:
        f.seek(offset)
        f.write(struct.pack('<ii', nr, nc))
        f.write(arr.tobytes())
    return bytes_written

def stitch_opq_binaries(
    bucket_prefixes: List[Path],
    bucket_sizes: List[int],
    out_prefix: Path,
    verbose: bool = True
):
    """Stitches bucket-wise OPQ files into unified DiskANN files."""
    num_buckets = len(bucket_prefixes)
    D = sum(bucket_sizes)

    # 1. Stitch Rotation Matrices (Block-Diagonal Matrix)
    rot_mats = []
    for prefix, b_dim in zip(bucket_prefixes, bucket_sizes):
        rot_file = Path(str(prefix) + "_pq_pivots.bin_rotation_matrix.bin")
        if not rot_file.exists():
            raise FileNotFoundError(f"Rotation matrix file not found: {rot_file}")
        arr, nr, nc = load_bin_numpy_float(rot_file)
        assert nr == b_dim and nc == b_dim, f"Rotation matrix dim mismatch: expected {b_dim}x{b_dim}, got {nr}x{nc}"
        rot_mats.append(arr)

    # Build D x D block diagonal matrix
    R_global = np.zeros((D, D), dtype=np.float32)
    curr_idx = 0
    for R_k, b_dim in zip(rot_mats, bucket_sizes):
        R_global[curr_idx : curr_idx + b_dim, curr_idx : curr_idx + b_dim] = R_k
        curr_idx += b_dim

    out_rot_file = Path(str(out_prefix) + "_pq_pivots.bin_rotation_matrix.bin")
    save_bin_numpy(out_rot_file, R_global)
    if verbose:
        print(f"Stitched rotation matrix to {out_rot_file} ({D}x{D})", flush=True)

    # 2. Stitch Compressed Codes (Column-wise Concatenation of bytes)
    comp_codes = []
    num_pts = -1
    total_chunks = 0
    for prefix in bucket_prefixes:
        comp_file = Path(str(prefix) + "_pq_compressed.bin")
        with open(comp_file, 'rb') as f:
            npts, chunks = struct.unpack('<II', f.read(8))
            if num_pts == -1:
                num_pts = npts
            else:
                assert num_pts == npts, "Points count mismatch across bucket compressed files"
            total_chunks += chunks
            data = np.frombuffer(f.read(), dtype=np.uint8).reshape(npts, chunks)
            comp_codes.append(data)

    merged_codes = np.hstack(comp_codes)
    out_comp_file = Path(str(out_prefix) + "_pq_compressed.bin")
    with open(out_comp_file, 'wb') as f:
        f.write(struct.pack('<II', num_pts, total_chunks))
        f.write(merged_codes.tobytes())
    if verbose:
        print(f"Stitched compressed codes to {out_comp_file} (points={num_pts}, chunks={total_chunks})", flush=True)

    # 3. Stitch Pivots File (Stitching full_pivot_data, centroid, and chunk_offsets)
    centroids = []
    pivots_list = []
    offsets_list = []
    curr_offset_shift = 0

    for prefix, b_dim in zip(bucket_prefixes, bucket_sizes):
        pivots_file = Path(str(prefix) + "_pq_pivots.bin")
        
        # Read the 32-byte offsets block (skipping the 8-byte save_bin header (4, 1) at offset 0)
        with open(pivots_file, 'rb') as f:
            f.seek(8)
            offsets = struct.unpack('<QQQQ', f.read(32))
        
        # Load pivots (size [256, b_dim])
        piv, _, _ = load_bin_numpy_float(pivots_file, offset=offsets[0])
        pivots_list.append(piv)

        # Load centroid (size [b_dim, 1])
        cent, _, _ = load_bin_numpy_float(pivots_file, offset=offsets[1])
        centroids.append(cent.flatten())

        # Load chunk offsets
        chunk_offs, nr, _ = load_bin_numpy_uint32(pivots_file, offset=offsets[2])
        chunk_offs = chunk_offs.flatten()
        
        # Adjust chunk offsets for the global coordinate shift
        if len(offsets_list) == 0:
            offsets_list.extend(chunk_offs)
        else:
            # Skip the leading 0 of the current chunk offsets and shift the rest
            offsets_list.extend(chunk_offs[1:] + curr_offset_shift)

        curr_offset_shift += b_dim

    # Concatenate fields
    full_pivot_data = np.hstack(pivots_list)  # [256, D]
    centroid_global = np.concatenate(centroids).reshape(-1, 1)  # [D, 1]
    chunk_offsets_global = np.array(offsets_list, dtype=np.uint32).reshape(-1, 1) # [M+1, 1]

    # Calculate exact offsets in stitched file
    HEADER_SIZE = 4096
    out_pivots_file = Path(str(out_prefix) + "_pq_pivots.bin")
    
    # Initialize pivots file with 4096 zero bytes
    with open(out_pivots_file, 'wb') as f:
        f.write(b'\x00' * HEADER_SIZE)

    # Write each field and record byte offsets
    offset_pivots = HEADER_SIZE
    bytes_piv = save_bin_numpy(out_pivots_file, full_pivot_data, offset=offset_pivots, mode='r+b')
    
    offset_centroid = offset_pivots + bytes_piv
    bytes_cent = save_bin_numpy(out_pivots_file, centroid_global, offset=offset_centroid, mode='r+b')
    
    offset_offsets = offset_centroid + bytes_cent
    bytes_offs = save_bin_numpy(out_pivots_file, chunk_offsets_global, offset=offset_offsets, mode='r+b')
    
    total_size = offset_offsets + bytes_offs

    # Write offsets block back (with 8-byte (4, 1) save_bin header at offset 0, then 32 bytes offsets)
    with open(out_pivots_file, 'r+b') as f:
        f.seek(0)
        f.write(struct.pack('<ii', 4, 1))  # nr = 4, nc = 1
        f.write(struct.pack('<QQQQ', offset_pivots, offset_centroid, offset_offsets, total_size))

    if verbose:
        print(f"Stitched pivots file to {out_pivots_file} (total size={total_size}B)", flush=True)

def train_and_quantize_block_opq(cfg: Config, allocation: List[int], tag: str) -> Tuple[Path, List[Path]]:
    """Slices vectors, runs standard C++ OPQ independently per bucket (with cache), and stitches results."""
    # 1. Generate temp directories and output paths
    step_dir = cfg.work_dir / f"step_{tag}"
    step_dir.mkdir(parents=True, exist_ok=True)

    base_slices = [step_dir / f"base_b{i}.bin" for i in range(cfg.num_buckets)]
    query_slices = [step_dir / f"query_b{i}.bin" for i in range(cfg.num_buckets)]
    
    # 2. Slice base and query datasets
    slice_bin_file(cfg.base_file, base_slices, cfg.bucket_sizes, verbose=cfg.verbose)
    slice_bin_file(cfg.query_file, query_slices, cfg.bucket_sizes, verbose=cfg.verbose)

    # 3. Train OPQ independently per bucket
    bucket_prefixes = []
    artifacts = []
    
    cache_dir = cfg.opq_cache_dir
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)

    for i, (b_base, b_query, b_size, M_k) in enumerate(zip(base_slices, query_slices, cfg.bucket_sizes, allocation)):
        b_prefix = step_dir / f"opq_b{i}"
        bucket_prefixes.append(b_prefix)
        
        # Define the cache file paths
        cache_pivots = cache_dir / f"bucket_{i}_chunk_{M_k}_s{cfg.sampling_rate}_pq_pivots.bin" if cache_dir else None
        cache_rotmat = cache_dir / f"bucket_{i}_chunk_{M_k}_s{cfg.sampling_rate}_pq_pivots.bin_rotation_matrix.bin" if cache_dir else None
        cache_compressed = cache_dir / f"bucket_{i}_chunk_{M_k}_s{cfg.sampling_rate}_pq_compressed.bin" if cache_dir else None
        
        # Target paths in step_dir
        tgt_pivots = Path(str(b_prefix) + "_pq_pivots.bin")
        tgt_rotmat = Path(str(b_prefix) + "_pq_pivots.bin_rotation_matrix.bin")
        tgt_compressed = Path(str(b_prefix) + "_pq_compressed.bin")
        tgt_inflated = Path(str(b_prefix) + "_pq_compressed.bin_inflated.bin")
        
        use_cache = False
        if cache_dir and cache_pivots.exists() and cache_rotmat.exists() and cache_compressed.exists():
            use_cache = True
            
        if use_cache:
            if cfg.verbose:
                print(f"[CACHE HIT] Copying cached OPQ for bucket {i} with {M_k} chunks (sampling rate {cfg.sampling_rate})", flush=True)
            shutil.copy2(cache_pivots, tgt_pivots)
            shutil.copy2(cache_rotmat, tgt_rotmat)
            shutil.copy2(cache_compressed, tgt_compressed)
        else:
            if cfg.verbose:
                if cache_dir:
                    print(f"[CACHE MISS] Training OPQ for bucket {i} with {M_k} chunks...", flush=True)
                else:
                    print(f"Training OPQ for bucket {i} with {M_k} chunks (no cache)...", flush=True)
            # Invoke standard generate_pq tool with OPQ parameter set to 1
            gen_tool = cfg.tools_dir / "generate_pq"
            cmd = [
                str(gen_tool),
                "float",
                str(b_base),
                str(b_prefix),
                str(M_k),
                str(cfg.sampling_rate),
                "1"  # OPQ=1
            ]
            run_cmd(cmd, verbose=cfg.verbose)
            
            # Save to cache if enabled
            if cache_dir:
                shutil.copy2(tgt_pivots, cache_pivots)
                shutil.copy2(tgt_rotmat, cache_rotmat)
                shutil.copy2(tgt_compressed, cache_compressed)

        # Track intermediate bucket files
        artifacts.extend([
            b_base,
            b_query,
            tgt_pivots,
            tgt_rotmat,
            tgt_compressed,
            tgt_inflated
        ])

    # 4. Stitch everything together
    out_prefix = cfg.work_dir / f"{cfg.pq_prefix_base}_{tag}"
    stitch_opq_binaries(bucket_prefixes, cfg.bucket_sizes, out_prefix, verbose=cfg.verbose)

    # Save outputs
    compressed = Path(str(out_prefix) + "_pq_compressed.bin")
    pivots = Path(str(out_prefix) + "_pq_pivots.bin")
    rotmat = Path(str(out_prefix) + "_pq_pivots.bin_rotation_matrix.bin")

    # Generate inflated/dequantized file for recall evaluation
    # We construct the inflated file by loading compressed codes and reconstructing floats
    # DiskANN provides generate_pq_data_from_pivots but it saves inflated bin during the execution.
    # To run compute_groundtruth we need the _inflated.bin. Let's see if generate_pq_data_from_pivots
    # can do that. Yes, standard C++ generate_pq writes the inflated file when use_opq=true,
    # but we stitched the outputs. How do we inflate the STITCHED file?
    # We must run a C++ query preprocessor or write a quick Python dequantization helper.
    # Let's write a Python dequantization script to inflate the stitched PQ compressed vectors
    # to avoid changing C++ codebase.
    inflated = Path(str(compressed) + "_inflated.bin")
    inflate_stitched_opq(compressed, pivots, rotmat, inflated, cfg.dim, verbose=cfg.verbose)

    artifacts.extend([compressed, pivots, rotmat, inflated])
    return out_prefix, artifacts

def inflate_stitched_opq(compressed_path: Path, pivots_path: Path, rotmat_path: Path, out_path: Path, dim: int, verbose: bool = True):
    """Dequantizes/inflates the stitched compressed vectors back into rotated float32 vector space."""
    if verbose:
        print(f"Dequantizing stitched OPQ indices to {out_path}...", flush=True)

    # 1. Load chunk offsets and full pivots data
    with open(pivots_path, 'rb') as f:
        f.seek(8)
        offsets = struct.unpack('<QQQQ', f.read(32))

    full_pivots, _, _ = load_bin_numpy_float(pivots_path, offset=offsets[0]) # [256, dim]
    centroid, _, _ = load_bin_numpy_float(pivots_path, offset=offsets[1]) # [dim, 1]
    chunk_offsets, _, _ = load_bin_numpy_uint32(pivots_path, offset=offsets[2])
    chunk_offsets = chunk_offsets.flatten()
    centroid = centroid.flatten()

    # 2. Load compressed codes
    with open(compressed_path, 'rb') as f:
        npts, chunks = struct.unpack('<II', f.read(8))
        codes = np.frombuffer(f.read(), dtype=np.uint8).reshape(npts, chunks)

    # 3. Reconstruct rotated coordinates
    reconstructed = np.zeros((npts, dim), dtype=np.float32)
    for c in range(chunks):
        c_start = chunk_offsets[c]
        c_end = chunk_offsets[c + 1]
        
        # For each point, retrieve its codeword centroid
        pts_codewords = codes[:, c]
        chunk_centroids = full_pivots[pts_codewords, c_start:c_end]
        reconstructed[:, c_start:c_end] = chunk_centroids

    # 3.5 Rotate back to original space using the transpose of the rotation matrix (R_tr.T = R)
    if rotmat_path and rotmat_path.exists():
        if verbose:
            print(f"Applying back-rotation using {rotmat_path.name}...", flush=True)
        R_tr, _, _ = load_bin_numpy_float(rotmat_path)
        reconstructed = reconstructed @ R_tr.T
    else:
        raise FileNotFoundError(f"Rotation matrix not found at: {rotmat_path}. Required for OPQ back-rotation.")
    

    # 4. Add centroid back (since DiskANN adds translation back during query inflation)
    reconstructed += centroid

    # 5. Write standard float binary
    with open(out_path, 'wb') as f:
        write_fbin_header(f, npts, dim)
        f.write(reconstructed.tobytes())
    
    if verbose:
        print(f"Inflated file written: {out_path} ({npts} points, dim={dim})", flush=True)

def compute_quantized_gt(cfg: Config, inflated_file: Path, tag: str) -> Path:
    gt_out = cfg.work_dir / f"quantized_gt_{tag}.bin"
    gt_tool = cfg.tools_dir / "compute_groundtruth"
    cmd = [str(gt_tool), "--data_type", "float", "--dist_fn", "l2", "--base_file", str(inflated_file),
           "--query_file", str(cfg.query_file), "--gt_file", str(gt_out), "--K", str(cfg.k)]
    run_cmd(cmd, verbose=cfg.verbose)
    return gt_out

def compute_recall(cfg: Config, quantized_gt: Path) -> float:
    recall_tool = cfg.tools_dir / "calculate_recall"
    cmd = [str(recall_tool), str(cfg.raw_gt_file), str(quantized_gt), str(cfg.k)]
    out = run_cmd(cmd, verbose=cfg.verbose)
    m = RECALL_REGEX.search(out)
    if not m:
        raise RuntimeError("Failed to parse recall from output:\n" + out)
    return float(m.group(1))

def evaluate_block_opq_allocation(cfg: Config, allocation: List[int], tag: str) -> Tuple[float, IterRecord]:
    prefix_path, artifacts = train_and_quantize_block_opq(cfg, allocation, tag)
    compressed = Path(str(prefix_path) + "_pq_compressed.bin")
    inflated = Path(str(compressed) + "_inflated.bin")
    
    quant_gt = compute_quantized_gt(cfg, inflated, tag)
    recall = compute_recall(cfg, quant_gt)
    
    artifacts.append(quant_gt)
    
    if cfg.verbose:
        print("BLOCK_OPQ_EVAL", f"tag={tag}", f"alloc={allocation}", f"bytes={sum(allocation)}", f"recall={recall:.6f}", flush=True)

    return recall, IterRecord(
        iteration=-1,
        allocation=allocation.copy(),
        recall=recall,
        bytes_per_vec=sum(allocation),
        prefix=str(prefix_path),
        improved=False,
        tag=tag,
        artifacts=artifacts
    )

def cleanup_artifacts(records: List[IterRecord], preserve_allocation: List[int], verbose: bool):
    """Deletes temporary step artifacts except for the best configuration."""
    for rec in records:
        if rec.allocation == preserve_allocation:
            continue
        
        # Clean up files in IterRecord list
        for path in rec.artifacts:
            try:
                if path.exists():
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
            except Exception:
                pass
        
        # Also find and remove the subdirectory step_tag
        try:
            step_dir = Path(rec.prefix).parent / f"step_{rec.tag}"
            if step_dir.exists() and step_dir.is_dir():
                shutil.rmtree(step_dir)
        except Exception:
            pass

    if verbose:
        print("[CLEANUP] Deleted intermediate bucket directories and training artifacts.", flush=True)

# ----------------- TRACKS -----------------

def run_global_opq_baseline(cfg: Config) -> Tuple[float, Path]:
    """Track 1: Runs standard C++ OPQ without block-diagonal constraints (absolute recall upper bound)."""
    print("\n--- Running Track 1: Global (Whole) OPQ Baseline ---", flush=True)
    out_prefix = cfg.work_dir / "global_opq"
    
    gen_tool = cfg.tools_dir / "generate_pq"
    cmd = [
        str(gen_tool),
        "float",
        str(cfg.base_file),
        str(out_prefix),
        str(cfg.max_total_bytes), # Chunks = Target Bytes
        str(cfg.sampling_rate),
        "1" # OPQ = 1
    ]
    run_cmd(cmd, verbose=cfg.verbose)

    # In standard generate_pq, the C++ code outputs _pq_compressed.bin_inflated.bin
    # when use_opq=true. Let's find it.
    compressed = Path(str(out_prefix) + "_pq_compressed.bin")
    pivots = Path(str(out_prefix) + "_pq_pivots.bin")
    rotmat = Path(str(out_prefix) + "_pq_pivots.bin_rotation_matrix.bin")
    inflated = Path(str(compressed) + "_inflated.bin")
    if pivots.exists() and rotmat.exists() and compressed.exists():
        print("inflating global opq..", flush=True)
        if inflated.exists():
            try:
                inflated.unlink()
            except Exception:
                pass
        inflate_stitched_opq(compressed, pivots, rotmat, inflated, cfg.dim, verbose=cfg.verbose)
    else:
        raise FileNotFoundError(f"Track 1 files missing.")

    quant_gt = compute_quantized_gt(cfg, inflated, "global")
    recall = compute_recall(cfg, quant_gt)
    print(f"Track 1: Global (Whole) OPQ Recall@{cfg.k} = {recall:.6f}\n", flush=True)
    return recall, out_prefix

def run_block_uniform_opq_baseline(cfg: Config) -> Dict[int, float]:
    """Track 2: Runs block-diagonal OPQ with uniform chunk distribution across buckets for all budgets."""
    print("\n--- Running Track 2: Block-Diagonal Uniform OPQ Sweep ---", flush=True)
    
    uniform_recalls = {}
    byte_values = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
    
    for target_bytes in byte_values:
        if target_bytes > cfg.max_total_bytes:
            continue
            
        print(f"\n--- Uniform OPQ Baseline: {target_bytes} Bytes ---", flush=True)
        # Evenly distribute target_bytes among buckets
        base_alloc = target_bytes // cfg.num_buckets
        rem = target_bytes % cfg.num_buckets
        allocation = [base_alloc + (1 if i < rem else 0) for i in range(cfg.num_buckets)]
        
        print(f"Uniform allocation layout: {allocation}", flush=True)
        
        recall, rec = evaluate_block_opq_allocation(cfg, allocation, f"uniform_opq_{target_bytes}")
        uniform_recalls[target_bytes] = recall
        print(f"Bytes={target_bytes} (Uniform OPQ) - Recall@{cfg.k}: {recall:.6f}", flush=True)
        
        # Cleanup intermediate files for this uniform run to save space
        if not cfg.keep_all:
            cleanup_artifacts([rec], preserve_allocation=[], verbose=cfg.verbose)
            
    return uniform_recalls

def run_variable_block_opq_sweep(cfg: Config) -> Dict[str, Any]:
    """Track 3: Runs greedy search over block-diagonal OPQ allocations."""
    print("\n--- Running Track 3: Variable Block-Diagonal OPQ Sweeping ---", flush=True)
    
    history: List[IterRecord] = []
    
    # Start with initial uniform budget
    current_alloc = [cfg.initial_chunks for _ in range(cfg.num_buckets)]
    best_recall, rec = evaluate_block_opq_allocation(cfg, current_alloc, tag="init")
    rec.iteration = 0
    rec.improved = True
    history.append(rec)
    
    print(f"Iteration 0 (Initial uniform): {current_alloc} => recall={best_recall:.6f}", flush=True)
    
    prev_iteration_records: List[IterRecord] = [rec]
    candidates: List[Tuple[float, List[int], IterRecord]] = []
    
    try:
        for it in range(1, cfg.max_iters + 1):
            candidates = []
            
            # Generate candidates by incrementing allocation in each bucket
            for b in range(cfg.num_buckets):
                if current_alloc[b] + cfg.increment > cfg.max_per_bucket:
                    continue
                if sum(current_alloc) + cfg.increment > cfg.max_total_bytes:
                    continue
                    
                cand_alloc = current_alloc.copy()
                cand_alloc[b] += cfg.increment
                tag = f"it{it}_b{b}_plus{cfg.increment}"
                
                try:
                    recall, rec_cand = evaluate_block_opq_allocation(cfg, cand_alloc, tag=tag)
                except Exception as e:
                    print(f"[WARN] Candidate allocation {cand_alloc} failed: {e}", flush=True)
                    continue
                    
                rec_cand.iteration = it
                candidates.append((recall, cand_alloc, rec_cand))
    
            if not candidates:
                print("No more valid candidate allocations; stopping search.", flush=True)
                break
    
            # Sort candidates: highest recall first, tie-break on fewer bytes
            candidates.sort(key=lambda x: (-x[0], sum(x[1]), x[1]))
            best_cand_recall, best_cand_alloc, best_cand_rec = candidates[0]
    
            is_improvement = best_cand_recall > best_recall + 1e-9
            best_recall = best_cand_recall
            current_alloc = best_cand_alloc
            best_cand_rec.improved = is_improvement
            history.append(best_cand_rec)
            
            if is_improvement:
                print(f"Iteration {it}: improved recall -> {best_recall:.6f} with alloc {current_alloc}", flush=True)
            else:
                print(f"Iteration {it}: no improvement (best candidate recall={best_cand_recall:.6f}); continuing search.", flush=True)
    
            if not cfg.keep_all:
                cleanup_artifacts(prev_iteration_records, preserve_allocation=current_alloc, verbose=cfg.verbose)
            
            prev_iteration_records = [cand[2] for cand in candidates]
    finally:
        if not cfg.keep_all:
            to_clean = []
            for cand in candidates:
                to_clean.append(cand[2])
            to_clean.extend(prev_iteration_records)
            to_clean.extend(history)
            cleanup_artifacts(to_clean, preserve_allocation=current_alloc, verbose=cfg.verbose)
    
    result = {
        "final_allocation": current_alloc,
        "final_recall": best_recall,
        "history": [dataclasses.asdict(r) for r in history]
    }
    return result

# ----------------- MAIN -----------------

def parse_args(argv: List[str]) -> Config:
    p = argparse.ArgumentParser(description="Matryoshka Block-OPQ Pipeline Orchestrator")
    p.add_argument('--base_file', required=True)
    p.add_argument('--query_file', required=True)
    p.add_argument('--raw_gt_file', required=True)
    p.add_argument('--work_dir', required=True)
    p.add_argument('--tools_dir', required=True)
    p.add_argument('--k', type=int, default=100)
    p.add_argument('--num_buckets', type=int, default=8)
    p.add_argument('--sampling_rate', type=float, default=0.1)
    p.add_argument('--initial_chunks', type=int, default=8)
    p.add_argument('--increment', type=int, default=8)
    p.add_argument('--max_iters', type=int, default=50)
    p.add_argument('--max_per_bucket', type=int, default=384)
    p.add_argument('--max_total_bytes', type=int, default=384)
    p.add_argument('--keep_all', action='store_true')
    p.add_argument('--pq_prefix_base', default='opq_cfg')
    p.add_argument('--opq_cache_dir', default=None, help='Directory to cache intermediate bucket OPQ files.')
    p.add_argument('--clear_opq_cache', action='store_true', help='Clear the cache directory before starting.')
    args = p.parse_args(argv)
    
    cache_dir = Path(args.opq_cache_dir) if args.opq_cache_dir else Path(args.base_file).parent / "opq_cache"
    
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
        opq_cache_dir=cache_dir,
        clear_opq_cache=args.clear_opq_cache
    )

def infer_buckets(cfg: Config):
    _, dim_base = read_fbin_header(cfg.base_file)
    _, dim_query = read_fbin_header(cfg.query_file)
    if dim_base != dim_query:
        raise ValueError(f"Base and Query dims mismatch: {dim_base} vs {dim_query}")
    cfg.dim = dim_base
    
    base_size = cfg.dim // cfg.num_buckets
    rem = cfg.dim % cfg.num_buckets
    cfg.bucket_sizes = [base_size + (1 if i < rem else 0) for i in range(cfg.num_buckets)]
    if cfg.verbose:
        print(f"Dimension inferred: {cfg.dim}. Buckets layout: {cfg.bucket_sizes}", flush=True)

def aggregate_and_save_opq(cfg: Config, rec_track1: float, uniform_recalls: Dict[int, float], result_track3: Dict[str, Any]):
    print("\n==================================================")
    print("Aggregating OPQ Results & Generating Outputs...")
    print("==================================================")
    sys.stdout.flush()
    
    history = result_track3.get("history", [])
    
    # Organize greedy history by total bytes
    greedy_by_bytes = {}
    for entry in history:
        b_val = entry["bytes_per_vec"]
        rec = entry["recall"]
        alloc = entry["allocation"]
        # Keep the one with the highest recall for each total byte size
        if b_val not in greedy_by_bytes or rec > greedy_by_bytes[b_val]["recall"]:
            greedy_by_bytes[b_val] = {
                "recall": rec,
                "allocation": alloc
            }
            
    summary_results = []
    byte_values = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
    
    for bytes_val in byte_values:
        if bytes_val > cfg.max_total_bytes:
            continue
            
        uni_rec = uniform_recalls.get(bytes_val, 0.0)
        
        # Look up variable/greedy recall for the same byte size
        var_rec = 0.0
        var_alloc = []
        
        if bytes_val in greedy_by_bytes:
            var_rec = greedy_by_bytes[bytes_val]["recall"]
            var_alloc = greedy_by_bytes[bytes_val]["allocation"]
        else:
            # Fallback scan for closest evaluated size <= bytes_val
            best_fallback_bytes = -1
            for k in sorted(greedy_by_bytes.keys()):
                if k <= bytes_val:
                    best_fallback_bytes = k
            if best_fallback_bytes != -1:
                var_rec = greedy_by_bytes[best_fallback_bytes]["recall"]
                var_alloc = greedy_by_bytes[best_fallback_bytes]["allocation"]
                
        # Uniform allocation is target_bytes // num_buckets for each bucket
        uni_alloc = [bytes_val // cfg.num_buckets] * cfg.num_buckets
        
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
        "dataset": cfg.pq_prefix_base,
        "scheme": "OPQ",
        "max_total_bytes": cfg.max_total_bytes,
        "global_opq_recall_at_max": rec_track1,
        "results": summary_results
    }
    
    summary_json_path = cfg.work_dir / "opq_results.json"
    with open(summary_json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved results summary to: {summary_json_path}")
    
    # Generate LaTeX Table
    latex_table = make_latex_table_opq(cfg.pq_prefix_base, "OPQ", summary_results, rec_track1)
    
    summary_tex_path = cfg.work_dir / "opq_results_table.tex"
    with open(summary_tex_path, "w") as f:
        f.write(latex_table)
    print(f"Saved LaTeX table to: {summary_tex_path}")
    
    print("\n--------------------------------------------------")
    print("GENERATED LATEX TABLE:")
    print("--------------------------------------------------")
    print(latex_table)
    print("--------------------------------------------------\n")
    sys.stdout.flush()

def make_latex_table_opq(dataset, scheme, results, rec_track1):
    latex = []
    latex.append(r"\begin{table*}[htbp]")
    latex.append(r"    \centering")
    latex.append(f"    \\caption{{Comparison of Uniform vs. Variable (Greedy) Bit Allocation for Block-Diagonal {scheme} on {dataset}.}}")
    latex.append(f"    \\label{{tab:{dataset}_{scheme.lower()}_alloc}}")
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
        uni_rec = f"{r['uniform_recall'] * 100:.2f}"
        var_rec = f"{r['variable_recall'] * 100:.2f}"
        
        if r["uniform_recall"] > 0:
            imp_val = ((r["variable_recall"] - r["uniform_recall"]) / r["uniform_recall"]) * 100.0
            imp_str = f"+{imp_val:.2f}\\%" if imp_val >= 0 else f"{imp_val:.2f}\\%"
            if abs(imp_val - max_imp) < 1e-5:
                imp_str = f"\\textbf{{{imp_str}}}"
        else:
            imp_str = "0.00\\%"
            
        latex.append(f"        {bytes_val:<4} & {uni_alloc:<30} & {var_alloc:<34} & {uni_rec:<5} & {var_rec:<5} & {imp_str} \\\\")
        
    latex.append(r"        \midrule")
    latex.append(f"        \\multicolumn{{6}}{{l}}{{\\textbf{{Global OPQ Baseline Recall at {results[-1]['bytes']} Bytes:}} {rec_track1 * 100:.2f}\\%}} \\\\")
    latex.append(r"        \bottomrule")
    latex.append(r"    \end{tabular}")
    latex.append(r"    }")
    latex.append(r"\end{table*}")
    return "\n".join(latex)

def main(argv: List[str]) -> int:
    cfg = parse_args(argv)
    
    # Create work directory
    cfg.work_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear cache if requested
    if cfg.clear_opq_cache and cfg.opq_cache_dir and cfg.opq_cache_dir.exists():
        if cfg.verbose:
            print(f"[CACHE] Clearing OPQ cache at: {cfg.opq_cache_dir}", flush=True)
        shutil.rmtree(cfg.opq_cache_dir, ignore_errors=True)
        
    try:
        infer_buckets(cfg)
    except Exception as e:
        print(f"ERROR: failed bucket layout: {e}", flush=True)
        return 1
        
    try:
        # 1. Run Track 1: Global (Whole) OPQ Baseline
        rec_track1, global_out_prefix = run_global_opq_baseline(cfg)
        
        # 2. Run Track 2: Block-Diagonal Uniform OPQ Sweep
        uniform_recalls = run_block_uniform_opq_baseline(cfg)
        
        # 3. Run Track 3: Variable Block-Diagonal OPQ Sweep
        result_track3 = run_variable_block_opq_sweep(cfg)
        
        # 4. Aggregate results, write JSON and print LaTeX Table
        aggregate_and_save_opq(cfg, rec_track1, uniform_recalls, result_track3)
        
        # 5. Clean up Track 1 inflated and gt files to save space
        if not cfg.keep_all:
            global_compressed = Path(str(global_out_prefix) + "_pq_compressed.bin")
            global_inflated = Path(str(global_compressed) + "_inflated.bin")
            global_gt = cfg.work_dir / "quantized_gt_global.bin"
            for fpath in [global_inflated, global_gt]:
                if fpath.exists():
                    try:
                        fpath.unlink()
                    except Exception:
                        pass
            
    except CommandError as e:
        print(f"Execution command error: {e}", flush=True)
        return 2
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Unexpected pipeline failure: {e}", flush=True)
        return 3
        
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
