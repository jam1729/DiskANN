#!/usr/bin/env python3
"""
Shared utilities for PQ bucket byte allocation search algorithms in DiskANN.

This module provides common data structures, binary header parsers, process execution
helpers, chunk offset builders, and wrappers for DiskANN C++ PQ executables
(generate_pq_variable_chunks, compute_groundtruth, calculate_recall).
"""

from __future__ import annotations
import dataclasses
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

DEFAULT_NUM_BUCKETS = 8
DEFAULT_DIM_PLACEHOLDER = -1
RECALL_REGEX = re.compile(r"Avg\. recall@\d+ is ([0-9]*\.?[0-9]+)")


@dataclasses.dataclass
class Config:
    base_file: Path
    query_file: Path
    raw_gt_file: Path
    work_dir: Path
    tools_dir: Path
    # Derived at runtime
    dim: int = DEFAULT_DIM_PLACEHOLDER
    num_buckets: int = DEFAULT_NUM_BUCKETS
    bucket_sizes: List[int] = dataclasses.field(default_factory=list)  # length = num_buckets (sum == dim)
    k: int = 100
    sampling_rate: float = 0.1
    initial_chunks: int = 8
    increment: int = 8
    max_iters: int = 20
    max_per_bucket: int = 128
    max_total_bytes: int | None = None
    keep_all: bool = False
    sleep_wait: float = 0.5
    timeout_train: int = 0  # 0 => no extra timeout beyond process
    timeout_gt: int = 0
    timeout_recall: int = 0
    pq_prefix_base: str = "pq_cfg"
    inflate_suffix: str = "_pq_compressed.bin_inflated.bin"
    log_json: Path | None = None
    verbose: bool = True
    seed: int = 42


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


def _json_safe(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if dataclasses.is_dataclass(value):
        return _json_safe(dataclasses.asdict(value))
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


def save_json_log(log_path: Path | str, data: Any) -> None:
    """Save data to JSON file incrementally with directory creation."""
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with open(temp_path, "w") as f:
        json.dump(_json_safe(data), f, indent=2)
    temp_path.replace(path)


def run_cmd(cmd: List[str], timeout: int = 0, verbose: bool = True) -> str:
    if verbose:
        print("[CMD]", " ".join(cmd), flush=True)
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout or None,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise CommandError(f"Timeout running command: {' '.join(cmd)}")
    if proc.returncode != 0:
        raise CommandError(
            f"Command failed ({proc.returncode}): {' '.join(cmd)}\nOutput:\n{proc.stdout}"
        )
    return proc.stdout


def _read_fbin_header(path: Path) -> Tuple[int, int]:
    """Read DiskANN float32 binary header: returns (npts, dim)."""
    with open(path, "rb") as f:
        hdr = f.read(8)
        if len(hdr) != 8:
            raise ValueError(f"File too small for header: {path}")
        npts, dim = struct.unpack("<II", hdr)
        if npts == 0 or dim == 0:
            raise ValueError(f"Invalid header values in {path}: npts={npts} dim={dim}")
        return npts, dim


def _infer_dimension_and_buckets(cfg: Config) -> None:
    """Infer dataset dimension from base/query files and calculate per-bucket dimensions."""
    _, dim_base = _read_fbin_header(cfg.base_file)
    _, dim_query = _read_fbin_header(cfg.query_file)
    if dim_base != dim_query:
        raise ValueError(f"Base/query dim mismatch: {dim_base} vs {dim_query}")
    cfg.dim = dim_base
    if cfg.num_buckets <= 0 or cfg.num_buckets > cfg.dim:
        raise ValueError(
            f"num_buckets must be in (0, dim]; got {cfg.num_buckets} for dim={cfg.dim}"
        )
    base_bucket = cfg.dim // cfg.num_buckets
    rem = cfg.dim % cfg.num_buckets
    cfg.bucket_sizes = [
        base_bucket + (1 if i < rem else 0) for i in range(cfg.num_buckets)
    ]
    if cfg.verbose:
        print(f"Inferred dim={cfg.dim}; bucket_sizes={cfg.bucket_sizes}")


def load_sample_vectors(
    data_path: Path, sampling_rate: float, seed: int = 42
) -> np.ndarray:
    """Sample vectors uniformly from DiskANN float32 binary dataset."""
    npts, dim = _read_fbin_header(data_path)
    sample_npts = max(1, int(npts * sampling_rate))
    rng = np.random.default_rng(seed)
    indices = rng.choice(npts, size=sample_npts, replace=False)
    indices.sort()
    data = np.empty((sample_npts, dim), dtype=np.float32)
    with open(data_path, "rb") as f:
        for i, idx in enumerate(indices):
            f.seek(8 + idx * dim * 4)
            data[i] = np.fromfile(f, dtype=np.float32, count=dim)
    return data


def build_chunk_offsets(cfg: Config, allocation: List[int]) -> List[int]:
    """Generate cumulative chunk offsets across the full dimensionality.

    For each bucket i with dimensional span bucket_sizes[i], subdivide that span into
    allocation[i] contiguous chunks. If the bucket dimension is not divisible by the chunk
    count, remainder dims are distributed one each to the first R chunks (greedy balancing).

    Returns: list[int] of monotonically increasing offsets of length (total_chunks + 1),
    where offsets[0] == 0 and offsets[-1] == cfg.dim.
    """
    if not cfg.bucket_sizes:
        raise ValueError("Config bucket_sizes not initialized.")
    if len(allocation) != len(cfg.bucket_sizes):
        raise ValueError("Allocation length does not match number of buckets")
    offsets: List[int] = [0]
    cur = 0
    for bucket_dim, c in zip(cfg.bucket_sizes, allocation):
        if c <= 0:
            raise ValueError("Chunk count must be positive per bucket")
        base = bucket_dim // c
        rem = bucket_dim % c
        for i in range(c):
            size = base + (1 if i < rem else 0)
            cur += size
            offsets.append(cur)
    assert cur == cfg.dim, f"Final offset {cur} != inferred dim {cfg.dim}"
    return offsets


def write_offsets_file(offsets: List[int], path: Path) -> None:
    with open(path, "w") as f:
        f.write(" ".join(str(x) for x in offsets))
        f.write("\n")


def train_and_quantize(
    cfg: Config, allocation: List[int], tag: str
) -> Tuple[Path, Path, Path, Path]:
    """Run PQ training + compression for a given allocation and return
    (prefix_path, compressed_file, inflated_file, offsets_file)."""
    offsets = build_chunk_offsets(cfg, allocation)
    offsets_file = cfg.work_dir / f"offsets_{tag}.txt"
    write_offsets_file(offsets, offsets_file)
    prefix_path = cfg.work_dir / f"{cfg.pq_prefix_base}_{tag}"
    gen_tool = cfg.tools_dir / "generate_pq_variable_chunks"
    cmd = [
        str(gen_tool),
        "float",
        str(cfg.base_file),
        str(prefix_path),
        str(offsets_file),
        str(cfg.sampling_rate),
    ]
    run_cmd(cmd, timeout=cfg.timeout_train, verbose=cfg.verbose)
    compressed = Path(str(prefix_path) + "_pq_compressed.bin")
    inflated = Path(str(compressed) + "_inflated.bin")
    return prefix_path, compressed, inflated, offsets_file


def compute_quantized_gt(cfg: Config, inflated_file: Path, tag: str) -> Path:
    gt_out = cfg.work_dir / f"quantized_gt_{tag}.bin"
    gt_tool = cfg.tools_dir / "compute_groundtruth"
    cmd = [
        str(gt_tool),
        "--data_type",
        "float",
        "--dist_fn",
        "l2",
        "--base_file",
        str(inflated_file),
        "--query_file",
        str(cfg.query_file),
        "--gt_file",
        str(gt_out),
        "--K",
        str(cfg.k),
    ]
    run_cmd(cmd, timeout=cfg.timeout_gt, verbose=cfg.verbose)
    return gt_out


def compute_recall(cfg: Config, quantized_gt: Path) -> float:
    recall_tool = cfg.tools_dir / "calculate_recall"
    cmd = [str(recall_tool), str(cfg.raw_gt_file), str(quantized_gt), str(cfg.k)]
    out = run_cmd(cmd, timeout=cfg.timeout_recall, verbose=cfg.verbose)
    m = RECALL_REGEX.search(out)
    if not m:
        raise RuntimeError("Failed to parse recall from output:\n" + out)
    return float(m.group(1))


def evaluate_allocation(
    cfg: Config, allocation: List[int], tag: str
) -> Tuple[float, IterRecord]:
    prefix_path, compressed, inflated, offsets_file = train_and_quantize(
        cfg, allocation, tag
    )
    if not inflated.exists():
        raise FileNotFoundError(
            f"Inflated file not found: {inflated}. Rebuild with SAVE_INFLATED_PQ defined."
        )
    quant_gt = compute_quantized_gt(cfg, inflated, tag)
    recall = compute_recall(cfg, quant_gt)
    if cfg.verbose:
        print(
            "PQ_EVAL",
            f"tag={tag}",
            f"alloc={allocation}",
            f"bytes={sum(allocation)}",
            f"recall={recall:.6f}",
            flush=True,
        )
    artifacts = [
        compressed,
        inflated,
        quant_gt,
        offsets_file,
        prefix_path.with_name(prefix_path.name + "_pq_pivots.bin"),
    ]
    return recall, IterRecord(
        iteration=-1,
        allocation=allocation.copy(),
        recall=recall,
        bytes_per_vec=sum(allocation),
        prefix=str(prefix_path),
        improved=False,
        tag=tag,
        artifacts=artifacts,
    )


def _cleanup_iteration(
    records: List[IterRecord], preserve_allocation: List[int], verbose: bool
) -> None:
    """Delete artifact files for a completed iteration except those matching preserve_allocation."""
    preserved = preserve_allocation
    for rec in records:
        if rec.allocation == preserved:
            continue
        for path in rec.artifacts:
            try:
                if path and path.exists():
                    path.unlink()
            except Exception:
                pass
        try:
            prefix = Path(rec.prefix)
            base = prefix.name
            parent = prefix.parent
            if parent.exists():
                for f in parent.glob(base + "*"):
                    if f.is_file():
                        try:
                            f.unlink()
                        except Exception:
                            pass
        except Exception:
            pass
    if verbose:
        print("[CLEANUP] Removed artifacts for non-optimal configurations.")
