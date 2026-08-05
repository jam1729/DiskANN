#!/usr/bin/env python3
"""
K-Means Tau-based PQ Bucket Byte Allocation Search for DiskANN.

Algorithm Overview
------------------
1. Set an error threshold tau for k-means.
2. For each bucket i, binary search on chunk count k_i in [1, max_per_bucket] such that
   the k-means quantization cost (SSE) falls below tau.
3. Compute allocation:
   - Weighted mode (default): bytes per bucket are allocated weighted based on k_i, summing to B total bytes.
   - Exact budget mode (--exact_budget): binary search over tau such that sum(k_i) == B.
     Bucket i receives exactly k_i bytes.
4. Evaluate the resulting allocation using DiskANN C++ tools (generate_pq_variable_chunks,
   compute_groundtruth, calculate_recall) to measure recall@K.
5. Log structured intermediate trajectory incrementally to JSON for plotting.
"""

from __future__ import annotations
import argparse
import dataclasses
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

# Optimized k-means backends: FAISS (fastest C++/AVX), Scikit-Learn (Cython), or fallback to NumPy
try:
    import faiss
    _KMEANS_BACKEND = "faiss"
except ImportError:
    try:
        from sklearn.cluster import KMeans
        _KMEANS_BACKEND = "sklearn"
    except ImportError:
        _KMEANS_BACKEND = "numpy"

from pq_bucket_utils import (
    Config,
    IterRecord,
    CommandError,
    save_json_log,
    _infer_dimension_and_buckets,
    load_sample_vectors,
    evaluate_allocation,
    DEFAULT_NUM_BUCKETS,
)


def _fit_single_chunk_kmeans_faiss(
    X_sub: np.ndarray, num_centers: int = 256, max_iters: int = 15, seed: int = 42
) -> float:
    """Fit 256-center k-means using FAISS C++ engine (blazing fast).

    FAISS handles multi-core OpenMP parallelization natively in C++.
    """
    N, D_sub = X_sub.shape
    if N <= num_centers:
        # Fewer training vectors than clusters: zero quantization error
        return 0.0
    
    # FAISS requires C-contiguous float32 arrays
    X_sub = np.ascontiguousarray(X_sub, dtype=np.float32)
    kmeans = faiss.Kmeans(D_sub, num_centers, niter=max_iters, verbose=False, seed=seed)
    kmeans.train(X_sub)
    
    # Compute quantization error (sum of squared L2 distances)
    _, I = kmeans.index.search(X_sub, 1)
    centroids = kmeans.centroids
    dists = np.sum((X_sub - centroids[I.ravel()]) ** 2, axis=1)
    return float(np.sum(dists))


def _fit_single_chunk_kmeans_sklearn(
    X_sub: np.ndarray, num_centers: int = 256, max_iters: int = 15, seed: int = 42
) -> float:
    """Fit 256-center k-means using Scikit-Learn C/Cython engine (Elkan algorithm)."""
    N, D_sub = X_sub.shape
    if N <= num_centers:
        return 0.0

    from sklearn.cluster import KMeans
    km = KMeans(
        n_clusters=num_centers,
        max_iter=max_iters,
        n_init=1,
        random_state=seed,
        algorithm="elkan",
    ).fit(X_sub)
    return float(km.inertia_)


def _fit_single_chunk_kmeans_numpy(
    X_sub: np.ndarray, num_centers: int = 256, max_iters: int = 15, seed: int = 42
) -> float:
    """Fit 256-center k-means using vectorized NumPy fallback with np.add.at centroid updates."""
    N, D_sub = X_sub.shape
    if N <= num_centers:
        return 0.0

    rng = np.random.default_rng(seed)
    init_indices = rng.choice(N, size=num_centers, replace=False)
    centroids = X_sub[init_indices].copy()
    x_norms = np.sum(X_sub ** 2, axis=1)

    for iteration in range(max_iters):
        # L2 squared distance matrix: ||x||^2 + ||c||^2 - 2 * x @ c^T
        c_norms = np.sum(centroids ** 2, axis=1)
        dists = x_norms[:, None] + c_norms[None, :] - 2.0 * (X_sub @ centroids.T)
        np.maximum(dists, 0.0, out=dists)

        labels = np.argmin(dists, axis=1)

        # Vectorized centroid mean calculation
        new_centroids = np.empty_like(centroids)
        counts = np.bincount(labels, minlength=num_centers)
        
        np.ndarray.fill(new_centroids, 0.0)
        np.add.at(new_centroids, labels, X_sub)
        
        nonzero_mask = counts > 0
        new_centroids[nonzero_mask] /= counts[nonzero_mask, None]
        
        # Handle empty clusters by re-initializing to random vectors
        empty_indices = np.where(~nonzero_mask)[0]
        if len(empty_indices) > 0:
            rand_indices = rng.choice(N, size=len(empty_indices), replace=False)
            new_centroids[empty_indices] = X_sub[rand_indices]

        if np.allclose(centroids, new_centroids, atol=1e-5):
            centroids = new_centroids
            break
        centroids = new_centroids

    # Final sum of squared L2 quantization errors
    c_norms = np.sum(centroids ** 2, axis=1)
    dists = x_norms[:, None] + c_norms[None, :] - 2.0 * (X_sub @ centroids.T)
    np.maximum(dists, 0.0, out=dists)
    min_dists = np.min(dists, axis=1)
    return float(np.sum(min_dists))


def _fit_single_chunk_kmeans(
    X_sub: np.ndarray, num_centers: int = 256, max_iters: int = 15, seed: int = 42
) -> float:
    """Dispatch to fastest available k-means engine: FAISS -> Scikit-Learn -> NumPy."""
    if _KMEANS_BACKEND == "faiss":
        return _fit_single_chunk_kmeans_faiss(X_sub, num_centers, max_iters, seed)
    elif _KMEANS_BACKEND == "sklearn":
        return _fit_single_chunk_kmeans_sklearn(X_sub, num_centers, max_iters, seed)
    else:
        return _fit_single_chunk_kmeans_numpy(X_sub, num_centers, max_iters, seed)


def compute_bucket_kmeans_cost(
    X_bucket: np.ndarray,
    chunk_count: int,
    kmeans_iters: int = 15,
    seed: int = 42,
) -> float:
    """Compute total k-means SSE for a bucket partitioned into chunk_count contiguous sub-chunks.

    Sub-chunk boundaries are allocated evenly using remainder distribution (+1 to first R chunks).
    FAISS / C++ engines handle parallel execution cleanly and efficiently across CPU threads.
    """
    N, D_bucket = X_bucket.shape
    if chunk_count <= 0:
        raise ValueError("chunk_count must be >= 1")
    if chunk_count > D_bucket:
        chunk_count = D_bucket

    base_dim = D_bucket // chunk_count
    rem_dim = D_bucket % chunk_count

    chunk_spans: List[Tuple[int, int]] = []
    cur = 0
    for i in range(chunk_count):
        size = base_dim + (1 if i < rem_dim else 0)
        chunk_spans.append((cur, cur + size))
        cur += size

    sse_total = 0.0
    for i, (start_d, end_d) in enumerate(chunk_spans):
        X_sub = X_bucket[:, start_d:end_d]
        sse_total += _fit_single_chunk_kmeans(
            X_sub, num_centers=256, max_iters=kmeans_iters, seed=seed + i
        )

    return float(sse_total)


def find_k_for_bucket(
    X_bucket: np.ndarray,
    tau: float,
    max_k: int,
    cost_cache: Dict[int, float],
    kmeans_iters: int = 15,
    seed: int = 42,
) -> Tuple[int, float]:
    """Binary search for minimal k in [1, max_k] such that bucket k-means cost <= tau.

    Returns (k_i, cost_i).
    """

    def get_cost(k: int) -> float:
        if k not in cost_cache:
            cost_cache[k] = compute_bucket_kmeans_cost(
                X_bucket, k, kmeans_iters=kmeans_iters, seed=seed + k
            )
        return cost_cache[k]

    low = 1
    high = max_k
    best_k = max_k

    while low <= high:
        mid = (low + high) // 2
        cost_mid = get_cost(mid)
        if cost_mid <= tau:
            best_k = mid
            high = mid - 1
        else:
            low = mid + 1

    return best_k, get_cost(best_k)


def allocate_bytes_weighted(
    k_vector: List[int], total_bytes: int
) -> List[int]:
    """Allocate total_bytes proportionally based on k_vector weights.

    Formula: alloc_i = max(1, round(total_bytes * k_i / sum(k)))
    Remainder adjusted on largest k_i so sum(alloc) == total_bytes.
    """
    num_buckets = len(k_vector)
    total_k = sum(k_vector)
    if total_k == 0:
        return [max(1, total_bytes // num_buckets) for _ in range(num_buckets)]

    raw_alloc = [max(1, int(round(total_bytes * k / total_k))) for k in k_vector]
    diff = total_bytes - sum(raw_alloc)

    if diff != 0:
        sorted_indices = sorted(range(num_buckets), key=lambda i: k_vector[i], reverse=True)
        step = 1 if diff > 0 else -1
        for idx in sorted_indices:
            if diff == 0:
                break
            if raw_alloc[idx] + step >= 1:
                raw_alloc[idx] += step
                diff -= step

    return raw_alloc


def binary_search_tau_exact_budget(
    bucket_samples: List[np.ndarray],
    total_budget: int,
    bucket_max_k: List[int],
    cost_caches: List[Dict[int, float]],
    kmeans_iters: int = 15,
    trajectory_log: List[Dict[str, Any]] | None = None,
    log_json_path: Path | None = None,
    verbose: bool = True,
) -> Tuple[float, List[int], List[float]]:
    """Binary search over tau such that sum(k_i(tau)) == total_budget.

    If step-function jumps yield sum(k_i) < total_budget, greedily add +1 chunk to buckets
    with the highest k-means error until sum(k_i) == total_budget.
    """
    num_buckets = len(bucket_samples)

    max_tau = 0.0
    min_tau = float("inf")

    # Compute bounds for binary search over tau
    for i in range(num_buckets):
        c1 = cost_caches[i].setdefault(
            1,
            compute_bucket_kmeans_cost(
                bucket_samples[i], 1, kmeans_iters=kmeans_iters
            ),
        )
        c_max = cost_caches[i].setdefault(
            bucket_max_k[i],
            compute_bucket_kmeans_cost(
                bucket_samples[i],
                bucket_max_k[i],
                kmeans_iters=kmeans_iters,
            ),
        )
        max_tau = max(max_tau, c1)
        min_tau = min(min_tau, c_max)

    if min_tau <= 0:
        min_tau = 1e-6

    low_tau = min_tau
    high_tau = max_tau * 1.5
    best_tau = high_tau
    best_k_vec: List[int] = [1] * num_buckets
    best_costs: List[float] = [0.0] * num_buckets

    if verbose:
        print(f"[BINARY SEARCH TAU] Starting binary search over tau in range [{low_tau:.2f}, {high_tau:.2f}] for budget B={total_budget}...")

    step_idx = 0
    for it in range(30):
        mid_tau = (low_tau + high_tau) / 2.0
        k_vec = []
        costs = []
        for i in range(num_buckets):
            ki, ci = find_k_for_bucket(
                bucket_samples[i],
                mid_tau,
                bucket_max_k[i],
                cost_caches[i],
                kmeans_iters=kmeans_iters,
            )
            k_vec.append(ki)
            costs.append(ci)

        sum_k = sum(k_vec)
        step_record = {
            "step": step_idx,
            "tau": float(mid_tau),
            "k_vector": k_vec.copy(),
            "sum_k": int(sum_k),
            "per_bucket_errors": costs.copy(),
        }
        if trajectory_log is not None:
            trajectory_log.append(step_record)
            if log_json_path:
                save_json_log(log_json_path, {"binary_search_trajectory": trajectory_log})
        step_idx += 1

        if verbose:
            print(f"  [Iter {it:02d}] tau={mid_tau:.4f} -> sum(k)={sum_k} (target {total_budget}) k_vec={k_vec}")

        if sum_k == total_budget:
            best_tau = mid_tau
            best_k_vec = k_vec
            best_costs = costs
            break
        elif sum_k > total_budget:
            low_tau = mid_tau
        else:
            best_tau = mid_tau
            best_k_vec = k_vec
            best_costs = costs
            high_tau = mid_tau

    # Handle step-function shortfall if sum(k_vec) < total_budget
    sum_k = sum(best_k_vec)
    if sum_k < total_budget:
        shortfall = total_budget - sum_k
        if verbose:
            print(f"  [STEP ADJUSTMENT] sum(k)={sum_k} < target {total_budget}. Greedily adding +1 chunk to top {shortfall} highest-error buckets.")

        sorted_buckets = sorted(range(num_buckets), key=lambda i: best_costs[i], reverse=True)
        for i in range(shortfall):
            idx = sorted_buckets[i % num_buckets]
            if best_k_vec[idx] < bucket_max_k[idx]:
                best_k_vec[idx] += 1
                best_costs[idx] = cost_caches[idx].setdefault(
                    best_k_vec[idx],
                    compute_bucket_kmeans_cost(
                        bucket_samples[idx],
                        best_k_vec[idx],
                        kmeans_iters=kmeans_iters,
                    ),
                )

        if verbose:
            print(f"  [STEP ADJUSTMENT DONE] Adjusted k_vec={best_k_vec} (sum={sum(best_k_vec)})")

    return best_tau, best_k_vec, best_costs


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(description="K-Means Tau-based PQ Bucket Search")
    p.add_argument("--base_file", required=True)
    p.add_argument("--query_file", required=True)
    p.add_argument("--raw_gt_file", required=True)
    p.add_argument("--work_dir", required=True)
    p.add_argument("--tools_dir", required=True)
    p.add_argument("--k", type=int, default=100, help="Recall@K threshold")
    p.add_argument("--num_buckets", type=int, default=DEFAULT_NUM_BUCKETS)
    p.add_argument("--total_bytes", type=int, default=64, help="Target total byte budget B across vectors")
    p.add_argument("--sampling_rate", type=float, default=0.1)
    p.add_argument("--tau", type=float, default=None, help="Fixed k-means error threshold tau (for weighted mode)")
    p.add_argument("--exact_budget", action="store_true", help="Binary search over tau to satisfy sum(k_i) == total_bytes")
    p.add_argument("--max_per_bucket", type=int, default=128)
    p.add_argument("--kmeans_iters", type=int, default=15)
    p.add_argument("--num_threads", type=int, default=None, help="Number of worker threads for parallel k-means")
    p.add_argument("--log_json", help="Path to output structured trajectory JSON")
    p.add_argument("--keep_all", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--seed", type=int, default=42)

    args = p.parse_args(argv)
    verbose = not args.quiet

    if args.num_threads:
        os.environ["OMP_NUM_THREADS"] = str(args.num_threads)
        if _KMEANS_BACKEND == "faiss":
            faiss.omp_set_num_threads(args.num_threads)

    cfg = Config(
        base_file=Path(args.base_file),
        query_file=Path(args.query_file),
        raw_gt_file=Path(args.raw_gt_file),
        work_dir=Path(args.work_dir),
        tools_dir=Path(args.tools_dir),
        num_buckets=args.num_buckets,
        k=args.k,
        sampling_rate=args.sampling_rate,
        max_per_bucket=args.max_per_bucket,
        max_total_bytes=args.total_bytes,
        keep_all=args.keep_all,
        log_json=Path(args.log_json) if args.log_json else None,
        verbose=verbose,
        seed=args.seed,
    )

    for path_attr in ("base_file", "query_file", "raw_gt_file", "tools_dir"):
        p_val = getattr(cfg, path_attr)
        if not p_val.exists():
            print(f"ERROR: {path_attr} not found: {p_val}")
            return 1

    try:
        _infer_dimension_and_buckets(cfg)
    except Exception as e:
        print(f"ERROR inferring dimensions: {e}")
        return 1

    cfg.work_dir.mkdir(parents=True, exist_ok=True)
    log_json_path = cfg.log_json

    if verbose:
        print(f"Using k-means backend: '{_KMEANS_BACKEND.upper()}'")
        print(f"Loading sampled dataset ({cfg.sampling_rate * 100:.1f}%) for in-memory k-means error evaluation...")
    start_time = time.time()
    sample_vectors = load_sample_vectors(cfg.base_file, cfg.sampling_rate, seed=cfg.seed)
    if verbose:
        print(f"Loaded sample of shape {sample_vectors.shape} in {time.time() - start_time:.2f}s")

    bucket_samples: List[np.ndarray] = []
    bucket_max_k: List[int] = []
    cur_d = 0
    for b_size in cfg.bucket_sizes:
        bucket_samples.append(sample_vectors[:, cur_d : cur_d + b_size])
        bucket_max_k.append(min(b_size, cfg.max_per_bucket))
        cur_d += b_size

    cost_caches: List[Dict[int, float]] = [{} for _ in range(cfg.num_buckets)]
    trajectory_log: List[Dict[str, Any]] = []

    if args.exact_budget:
        mode = "exact_budget"
        tau, k_vec, costs = binary_search_tau_exact_budget(
            bucket_samples=bucket_samples,
            total_budget=cfg.max_total_bytes or 64,
            bucket_max_k=bucket_max_k,
            cost_caches=cost_caches,
            kmeans_iters=args.kmeans_iters,
            trajectory_log=trajectory_log,
            log_json_path=log_json_path,
            verbose=verbose,
        )
        final_allocation = k_vec.copy()
    else:
        mode = "weighted"
        if args.tau is None:
            c1_list = [
                compute_bucket_kmeans_cost(
                    bucket_samples[i], 1, kmeans_iters=args.kmeans_iters
                )
                for i in range(cfg.num_buckets)
            ]
            tau = float(np.mean(c1_list) / 2.0)
            if verbose:
                print(f"No tau specified. Calculated default tau={tau:.4f}")
        else:
            tau = args.tau

        k_vec = []
        costs = []
        for i in range(cfg.num_buckets):
            ki, ci = find_k_for_bucket(
                bucket_samples[i],
                tau,
                bucket_max_k[i],
                cost_caches[i],
                kmeans_iters=args.kmeans_iters,
            )
            k_vec.append(ki)
            costs.append(ci)

        final_allocation = allocate_bytes_weighted(
            k_vec, cfg.max_total_bytes or 64
        )
        trajectory_log.append({
            "step": 0,
            "tau": tau,
            "k_vector": k_vec.copy(),
            "sum_k": sum(k_vec),
            "per_bucket_errors": costs.copy(),
            "final_allocation": final_allocation.copy(),
        })

    if verbose:
        print("\n=== Algorithm Results ===")
        print(f"Backend: {_KMEANS_BACKEND.upper()}")
        print(f"Mode: {mode}")
        print(f"Selected tau: {tau:.6f}")
        print(f"K-vector (k_i per bucket): {k_vec} (sum = {sum(k_vec)})")
        print(f"Final byte allocation per bucket: {final_allocation} (sum = {sum(final_allocation)})")
        print("\nEvaluating recall with DiskANN C++ tools...")

    tag = "tau_kmeans_final"
    try:
        recall, record = evaluate_allocation(cfg, final_allocation, tag=tag)
    except CommandError as e:
        print(f"C++ Evaluation failed: {e}")
        return 2

    log_data = {
        "algorithm": "kmeans_tau_pq_bucket_search",
        "kmeans_backend": _KMEANS_BACKEND,
        "mode": mode,
        "total_bytes_target": cfg.max_total_bytes or 64,
        "tau": tau,
        "k_vector": k_vec,
        "sum_k": sum(k_vec),
        "per_bucket_errors": costs,
        "final_allocation": final_allocation,
        "recall_at_k": recall,
        "k": cfg.k,
        "binary_search_trajectory": trajectory_log,
        "record": dataclasses.asdict(record),
    }

    if log_json_path:
        save_json_log(log_json_path, log_data)
        if verbose:
            print(f"Structured trajectory JSON written to: {log_json_path}")

    print("\n=== Final Summary ===")
    print("Final allocation:", final_allocation)
    print(f"Final Recall@{cfg.k}: {recall:.6f}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
