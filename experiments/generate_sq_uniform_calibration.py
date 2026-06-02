#!/usr/bin/env python3
"""
Generate uniform/balanced Scalar Quantization (SQ) calibration files for a target byte budget.
"""
import argparse
import struct
import sys
from pathlib import Path
import numpy as np

def calibrate_dimensions(base_file: Path, sampling_rate: float) -> tuple[int, list[float], list[float]]:
    """Read base file header and sample vectors to compute dynamic range per dimension."""
    print(f"Calibrating dimensions from {base_file}...", flush=True)
    with open(base_file, 'rb') as f:
        npts = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        dim = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        
        sample_npts = max(1, int(npts * sampling_rate))
        
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
        for d in range(dim):
            if scale[d] <= 1e-9:
                scale[d] = 1.0
                
        return dim, bias, scale

def save_calibration(bias: list[float], scale: list[float], bit_widths: list[int], out_path: Path):
    ndims = len(bias)
    with open(out_path, 'wb') as f:
        f.write(struct.pack('<I', ndims))
        f.write(struct.pack(f'<{ndims}f', *bias))
        f.write(struct.pack(f'<{ndims}f', *scale))
        f.write(struct.pack(f'<{ndims}B', *bit_widths))

def main():
    parser = argparse.ArgumentParser(description="Generate balanced SQ calibration file for a target budget")
    parser.add_argument('--base_file', required=True, type=Path)
    parser.add_argument('--output_cal_file', required=True, type=Path)
    parser.add_argument('--target_bytes', required=True, type=int)
    parser.add_argument('--sampling_rate', type=float, default=0.1)
    parser.add_argument('--seed', type=int, default=42, help='Seed for random number generator')
    parser.add_argument('--allocation_strategy', choices=['front_load', 'stride'], default='stride',
                        help='Strategy to distribute bits across dimensions')
    args = parser.parse_args()
    
    # Set seed for reproducibility
    np.random.seed(args.seed)
    
    if not args.base_file.exists():
        print(f"ERROR: Base file not found: {args.base_file}")
        sys.exit(1)
        
    dim, bias, scale = calibrate_dimensions(args.base_file, args.sampling_rate)
    
    # Balance total bits = target_bytes * 8 as evenly as possible across dim dimensions using {0, 2, 4, 8} bits
    total_bits_needed = args.target_bytes * 8
    
    # Constraint check
    max_bits_possible = dim * 8
    if total_bits_needed > max_bits_possible:
        print(f"WARNING: Target budget of {args.target_bytes} bytes requires {total_bits_needed} bits, "
              f"but max possible with {dim} dimensions is {max_bits_possible} bits ({dim} bytes). "
              f"Capping at {dim} bytes.")
        total_bits_needed = max_bits_possible
        
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

    bit_widths = [0] * dim
    
    if args.allocation_strategy == 'stride':
        if total_bits_needed <= dim * 2:
            n2 = total_bits_needed // 2
            indices = select_k_indices(dim, n2)
            for idx in indices:
                bit_widths[idx] = 2
        elif total_bits_needed <= dim * 4:
            n4 = (total_bits_needed - 2 * dim) // 2
            indices = select_k_indices(dim, n4)
            indices_set = set(indices)
            for i in range(dim):
                bit_widths[i] = 4 if i in indices_set else 2
        else:
            n8 = (total_bits_needed - 4 * dim) // 4
            indices = select_k_indices(dim, n8)
            indices_set = set(indices)
            for i in range(dim):
                bit_widths[i] = 8 if i in indices_set else 4
    else:
        # Default: front_load
        if total_bits_needed <= dim * 2:
            # Levels: 0 and 2.
            # N2 * 2 = total_bits_needed => N2 = total_bits_needed // 2
            n2 = total_bits_needed // 2
            for i in range(min(n2, dim)):
                bit_widths[i] = 2
        elif total_bits_needed <= dim * 4:
            # Levels: 2 and 4.
            # N4 * 4 + (dim - N4) * 2 = total_bits_needed
            # 2 * N4 + 2 * dim = total_bits_needed => N4 = (total_bits_needed - 2 * dim) // 2
            n4 = (total_bits_needed - 2 * dim) // 2
            n4 = max(0, min(n4, dim))
            for i in range(dim):
                if i < n4:
                    bit_widths[i] = 4
                else:
                    bit_widths[i] = 2
        else:
            # Levels: 4 and 8.
            # N8 * 8 + (dim - N8) * 4 = total_bits_needed
            # 4 * N8 + 4 * dim = total_bits_needed => N8 = (total_bits_needed - 4 * dim) // 4
            n8 = (total_bits_needed - 4 * dim) // 4
            n8 = max(0, min(n8, dim))
            for i in range(dim):
                if i < n8:
                    bit_widths[i] = 8
                else:
                    bit_widths[i] = 4
                
    actual_bits = sum(bit_widths)
    actual_bytes = actual_bits / 8.0
    print(f"Target Bytes: {args.target_bytes}, Actual Bytes achieved: {actual_bytes}")
    print(f"Bit distribution across {dim} dimensions: "
          f"8-bit: {bit_widths.count(8)}, 4-bit: {bit_widths.count(4)}, "
          f"2-bit: {bit_widths.count(2)}, 0-bit: {bit_widths.count(0)}")
          
    args.output_cal_file.parent.mkdir(parents=True, exist_ok=True)
    save_calibration(bias, scale, bit_widths, args.output_cal_file)
    print(f"Successfully wrote calibration file to {args.output_cal_file}")

if __name__ == '__main__':
    main()
