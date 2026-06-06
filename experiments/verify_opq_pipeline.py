#!/usr/bin/env python3
"""
Unit test to verify the correctness of the slicing, stitching, and loading
utilities in run_opq_pipeline.py on a small mock dataset.
"""

import sys
from pathlib import Path
import struct
import shutil
import numpy as np

# Import functions from orchestrator directly
sys.path.append(str(Path(__file__).parent.parent / "scripts/dev"))
from run_opq_pipeline import (
    slice_bin_file,
    stitch_opq_binaries,
    load_bin_numpy_float,
    load_bin_numpy_uint32,
    save_bin_numpy,
    inflate_stitched_opq,
    write_fbin_header
)

def test_pipeline():
    print("=== Starting OPQ Pipeline Python Logic Verification ===", flush=True)

    # 1. Create a mock high-dimensional dataset
    npts = 100
    dim = 32
    data = np.random.randn(npts, dim).astype(np.float32)

    work_dir = Path(__file__).parent / "opq_test_tmp"
    work_dir.mkdir(exist_ok=True)
    base_file = work_dir / "base.bin"

    with open(base_file, 'wb') as f:
        f.write(struct.pack('<II', npts, dim))
        f.write(data.tobytes())

    # 2. Slice dataset into 4 buckets of size 8
    bucket_sizes = [8, 8, 8, 8]
    num_buckets = len(bucket_sizes)
    out_paths = [work_dir / f"base_b{i}.bin" for i in range(num_buckets)]

    slice_bin_file(base_file, out_paths, bucket_sizes, verbose=True)

    # Verify sliced files
    for i, (path, size) in enumerate(zip(out_paths, bucket_sizes)):
        with open(path, 'rb') as f:
            nr, nc = struct.unpack('<II', f.read(8))
            assert nr == npts, f"Bucket {i} point count mismatch"
            assert nc == size, f"Bucket {i} dim mismatch"
            slice_data = np.frombuffer(f.read(), dtype=np.float32).reshape(npts, size)
            
            # Verify slice values match original data slice
            orig_slice = data[:, i*8 : (i+1)*8]
            assert np.allclose(slice_data, orig_slice), f"Bucket {i} data values do not match original"

    print("Step 1: Slicer logic verified successfully.", flush=True)

    # 3. Create mock trained bucket outputs (centroids, offsets, rotation matrices, compressed indices)
    bucket_prefixes = [work_dir / f"b{i}_out" for i in range(num_buckets)]
    
    for i, size in enumerate(bucket_sizes):
        prefix = bucket_prefixes[i]
        
        # rotation_matrix: identity matrix [size, size]
        R_k = np.eye(size, dtype=np.float32)
        save_bin_numpy(Path(str(prefix) + "_pq_pivots.bin_rotation_matrix.bin"), R_k)
        
        # compressed: mock bytes (column chunks = 2, representing codewords)
        # For this mock, let's say M_k = 2 chunks per bucket
        M_k = 2
        comp_data = np.random.randint(0, 256, size=(npts, M_k), dtype=np.uint8)
        comp_file = Path(str(prefix) + "_pq_compressed.bin")
        with open(comp_file, 'wb') as f:
            f.write(struct.pack('<II', npts, M_k))
            f.write(comp_data.tobytes())

        # pivots:
        # cumul_bytes header offset allocation
        # full_pivots [256, size]
        # centroid [size, 1]
        # chunk_offsets [M_k + 1, 1]
        full_pivs = np.random.randn(256, size).astype(np.float32)
        centroid = np.random.randn(size, 1).astype(np.float32)
        chunk_offsets = np.array([0, 4, size], dtype=np.uint32).reshape(-1, 1)

        pivots_file = Path(str(prefix) + "_pq_pivots.bin")
        
        # Initialize
        HEADER_SIZE = 4096
        with open(pivots_file, 'wb') as f:
            f.write(b'\x00' * HEADER_SIZE)

        offset_piv = HEADER_SIZE
        bytes_piv = save_bin_numpy(pivots_file, full_pivs, offset=offset_piv, mode='r+b')

        offset_cent = offset_piv + bytes_piv
        bytes_cent = save_bin_numpy(pivots_file, centroid, offset=offset_cent, mode='r+b')

        offset_offs = offset_cent + bytes_cent
        bytes_offs = save_bin_numpy(pivots_file, chunk_offsets, offset=offset_offs, mode='r+b')

        total_size = offset_offs + bytes_offs

        # Save offsets with the correct (4, 1) header
        with open(pivots_file, 'r+b') as f:
            f.seek(0)
            f.write(struct.pack('<ii', 4, 1))
            f.write(struct.pack('<QQQQ', offset_piv, offset_cent, offset_offs, total_size))

    print("Step 2: Mock bucket outputs created.", flush=True)

    # 4. Run Stitching Engine
    out_prefix = work_dir / "stitched_global"
    stitch_opq_binaries(bucket_prefixes, bucket_sizes, out_prefix, verbose=True)

    # Verify Stitched outputs
    # A. Rotation matrix verification (should be global identity of size 32x32)
    stitched_rot_file = Path(str(out_prefix) + "_pq_pivots.bin_rotation_matrix.bin")
    R_global, nr, nc = load_bin_numpy_float(stitched_rot_file)
    assert nr == dim and nc == dim, "Stitched rotation matrix dimension mismatch"
    assert np.allclose(R_global, np.eye(dim)), "Stitched rotation matrix values incorrect"

    # B. Compressed codes verification
    stitched_comp_file = Path(str(out_prefix) + "_pq_compressed.bin")
    with open(stitched_comp_file, 'rb') as f:
        nr, nc = struct.unpack('<II', f.read(8))
        assert nr == npts, "Stitched compressed points mismatch"
        assert nc == sum([2, 2, 2, 2]), "Stitched compressed chunk count mismatch"
        comp_stitched = np.frombuffer(f.read(), dtype=np.uint8).reshape(nr, nc)
        assert comp_stitched.shape == (npts, 8), "Stitched compressed shape incorrect"

    # C. Pivots file verification
    stitched_pivots_file = Path(str(out_prefix) + "_pq_pivots.bin")
    with open(stitched_pivots_file, 'rb') as f:
        nr, nc = struct.unpack('<ii', f.read(8))
        assert nr == 4 and nc == 1, "Stitched pivots offsets header incorrect"
        offsets = struct.unpack('<QQQQ', f.read(32))

    full_pivots_g, nr, nc = load_bin_numpy_float(stitched_pivots_file, offset=offsets[0])
    assert nr == 256 and nc == dim, "Stitched pivots dimensions incorrect"

    centroid_g, nr, nc = load_bin_numpy_float(stitched_pivots_file, offset=offsets[1])
    assert nr == dim and nc == 1, "Stitched centroid dimensions incorrect"

    chunk_offsets_g, nr, nc = load_bin_numpy_uint32(stitched_pivots_file, offset=offsets[2])
    # Expected stitched chunk offsets:
    # local offsets are [0, 4, 8]. Stitching shifts them by b_dim = 8 each.
    # b0: 0, 4, 8
    # b1: 8 + 4 = 12, 8 + 8 = 16
    # b2: 16 + 4 = 20, 16 + 8 = 24
    # b3: 24 + 4 = 28, 24 + 8 = 32
    # So expected: [0, 4, 8, 12, 16, 20, 24, 28, 32]
    expected_offs = np.array([0, 4, 8, 12, 16, 20, 24, 28, 32], dtype=np.uint32)
    assert np.array_equal(chunk_offsets_g.flatten(), expected_offs), f"Stitched chunk offsets incorrect: {chunk_offsets_g.flatten()}"

    print("Step 3: Stitching engine verified successfully.", flush=True)

    # 5. Run Python Inflation
    inflated_file = Path(str(out_prefix) + "_pq_compressed.bin_inflated.bin")
    inflate_stitched_opq(
        Path(str(out_prefix) + "_pq_compressed.bin"),
        Path(str(out_prefix) + "_pq_pivots.bin"),
        stitched_rot_file,
        inflated_file,
        dim,
        verbose=True
    )

    # Verify inflated file shape and values
    with open(inflated_file, 'rb') as f:
        nr, nc = struct.unpack('<II', f.read(8))
        assert nr == npts and nc == dim, "Inflated file dimensions mismatch"
        infl_data = np.frombuffer(f.read(), dtype=np.float32).reshape(nr, nc)
        assert not np.any(np.isnan(infl_data)), "Inflated file contains NaNs"

    print("Step 4: Dequantization/Inflation verified successfully.", flush=True)

    # Cleanup temp directory
    shutil.rmtree(work_dir)
    print("\n=== ALL PIPELINE LOGIC TESTS PASSED SUCCESSFULLY! ===", flush=True)

if __name__ == '__main__':
    test_pipeline()
