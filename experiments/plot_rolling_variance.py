#!/usr/bin/env python3
"""
Generate and plot the rolling average variance across dimensions 
for Cohere v4 and OpenAI text-embedding-3-large models on MSMARCO, DBpedia, and Quora.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_full_variance(file_path: Path) -> tuple[int, np.ndarray]:
    """Read file header and compute dimension-wise variance across ALL vectors using memmap and chunked processing for memory safety."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    with open(file_path, 'rb') as f:
        npts = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        dim = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        
    print(f"Computing variance across all {npts:,} vectors of dimension {dim} from {file_path.parent.parent.name}/{file_path.parent.name}/{file_path.name}...")
    
    # Use memory map to read vectors without loading everything into memory at once
    data = np.memmap(file_path, dtype=np.float32, mode='r', offset=8, shape=(npts, dim))
    
    sum_x = np.zeros(dim, dtype=np.float64)
    sum_x2 = np.zeros(dim, dtype=np.float64)
    
    chunk_size = 25000
    for i in range(0, npts, chunk_size):
        chunk = data[i : min(i + chunk_size, npts)]
        # Accumulate sums in float64 for absolute precision
        sum_x += np.sum(chunk, axis=0, dtype=np.float64)
        sum_x2 += np.sum(chunk**2, axis=0, dtype=np.float64)
        
    mean = sum_x / npts
    mean_sq = sum_x2 / npts
    variances = mean_sq - mean**2
    
    # Close the memmap resource
    del data
    
    return dim, variances

def compute_rolling_mean(arr: np.ndarray, window: int) -> np.ndarray:
    """Compute rolling mean with window size using cumulative sum (handles boundaries beautifully in O(N))."""
    cumsum = np.cumsum(np.insert(arr, 0, 0.0))
    out = np.zeros_like(arr)
    for i in range(len(arr)):
        start = max(0, i - window + 1)
        out[i] = (cumsum[i + 1] - cumsum[start]) / (i + 1 - start)
    return out

def main():
    window = 128  # WINDOW SIZE (Can be changed to 64 or 128)
    
    embeddings_dir = Path("/home/jam1729/data/embeddings")
    
    datasets = {
        "dbpedia_entity_500k": "DBpedia Entity (500k)",
        "msmarco_500k": "MSMARCO (500k)",
        "quora_500k": "Quora (500k)"
    }
    
    models = {
        "cohere_v4": {
            "name": "Cohere v4 (1536 DIMS)",
            "dim": 1536
        },
        "openai_text_large_3": {
            "name": "OpenAI Text-Embedding-3-Large (3072 DIMS)",
            "dim": 3072
        }
    }
    
    # Setup Figure with premium academic styling
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = '#0f172a'
    plt.rcParams['axes.labelcolor'] = '#334155'
    plt.rcParams['xtick.color'] = '#475569'
    plt.rcParams['ytick.color'] = '#475569'
    
    fig, axes = plt.subplots(1, 2, figsize=(20, 9), dpi=300)
    
    # Harmonious Palette
    colors = {
        "dbpedia_entity_500k": "#0284c7",  # Tailwind Sky-600
        "msmarco_500k": "#f97316",         # Tailwind Orange-500
        "quora_500k": "#10b981"            # Tailwind Emerald-500
    }
    
    for ax_idx, (model_id, model_cfg) in enumerate(models.items()):
        ax = axes[ax_idx]
        dim_limit = model_cfg["dim"]
        
        # 1. Plot the rolling average line for each dataset first
        for ds_id, ds_label in datasets.items():
            base_file = embeddings_dir / ds_id / model_id / "base.bin"
            try:
                dim, vars_raw = load_full_variance(base_file)
                rolling_vars = compute_rolling_mean(vars_raw, window=window)
                
                # Plot the rolling average line skipping the first 30 dimensions
                skip_dims = 32
                ax.plot(np.arange(skip_dims, dim), rolling_vars[skip_dims:], label=ds_label, 
                        color=colors[ds_id], linewidth=2.2, zorder=3)
            except Exception as e:
                print(f"Error processing {ds_id} for {model_id}: {e}")
                
        # Subplot Titles and Styling
        ax.set_title(model_cfg["name"], fontsize=30, pad=15, fontweight="bold", color='#1e293b')
        ax.set_xlabel("Dimension Index", fontsize=30, labelpad=8)
        if ax_idx == 0:
            ax.set_ylabel(f"Rolling Mean Variance (Window={window})", fontsize=30, labelpad=8)
        ax.tick_params(axis='both', which='major', labelsize=24)
        ax.set_xlim(32, dim_limit)
        ax.grid(True, which='both', linestyle=':', alpha=0.3, zorder=1)
        if ax_idx == 1:
            ax.legend(fontsize=25, loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()
    
    # Save the output with window prefix
    output_path = Path(f"/home/jam1729/DiskANN/experiments/{window}_variance_rolling_average_plot.pdf")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nSuccessfully generated and saved plot to: {output_path}")

if __name__ == '__main__':
    main()
