#!/usr/bin/env python3
"""
Generate and plot the rolling average variance across dimensions 
for both Cohere v4 and OpenAI text-embedding-3-large models on MSMARCO and DBpedia.
Highlights the 8 Contiguous Buckets.
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
        "msmarco_500k": "MSMARCO (500k)"
    }
    
    models = {
        "cohere_v4": {
            "name": "Cohere v4 (1536 DIMS, 8 Buckets = 192 dims/bucket)",
            "num_buckets": 8,
            "dim": 1536
        },
        "openai_text_large_3": {
            "name": "OpenAI Text-Embedding-3-Large (3072 DIMS, 8 Buckets = 384 dims/bucket)",
            "num_buckets": 8,
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
        "msmarco_500k": "#f97316"          # Tailwind Orange-500
    }
    
    for ax_idx, (model_id, model_cfg) in enumerate(models.items()):
        ax = axes[ax_idx]
        dim_limit = model_cfg["dim"]
        bucket_size = dim_limit // model_cfg["num_buckets"]
        
        # 1. Plot the rolling average line for each dataset first
        for ds_id, ds_label in datasets.items():
            base_file = embeddings_dir / ds_id / model_id / "base.bin"
            try:
                dim, vars_raw = load_full_variance(base_file)
                rolling_vars = compute_rolling_mean(vars_raw, window=window)
                
                # Plot the rolling average line
                ax.plot(np.arange(dim), rolling_vars, label=ds_label, 
                        color=colors[ds_id], linewidth=2.2, zorder=3)
            except Exception as e:
                print(f"Error processing {ds_id} for {model_id}: {e}")
                
        # Get y-limits after plotting to place text labels precisely at the top
        ymin, ymax = ax.get_ylim()
        label_y = ymin + 0.96 * (ymax - ymin)
        
        # 2. Draw bucket boundaries and shade alternate buckets subtly
        for b in range(model_cfg["num_buckets"]):
            start = b * bucket_size
            end = (b + 1) * bucket_size
            if b % 2 == 1:
                # Use a soft Slate-100 color for high-quality professional shading
                ax.axvspan(start, end, facecolor='#f8fafc', alpha=0.8, zorder=0)
            
            # Draw subtle vertical lines at bucket boundaries
            if b > 0:
                ax.axvline(start, color='#cbd5e1', linestyle=':', linewidth=1.5, zorder=1)
                # Position label beautifully at the top
                ax.text(start, label_y, f"dim {start}", color='#64748b', 
                        fontsize=8, rotation=90, verticalalignment='top', horizontalalignment='center', alpha=0.9, zorder=2)
        
        # Subplot Titles and Styling
        ax.set_title(model_cfg["name"], fontsize=14, fontweight='bold', pad=15, color='#1e293b')
        ax.set_xlabel("Dimension Index", fontsize=12, fontweight='bold', labelpad=8)
        ax.set_ylabel(f"Rolling Mean Variance (Window={window})", fontsize=12, fontweight='bold', labelpad=8)
        ax.set_xlim(0, dim_limit)
        ax.grid(True, which='both', linestyle=':', alpha=0.3, zorder=1)
        ax.legend(fontsize=11, loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()
    
    # Save the output with window prefix
    output_path = Path(f"/home/jam1729/DiskANN/experiments/{window}_variance_rolling_average_plot.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nSuccessfully generated and saved plot to: {output_path}")

if __name__ == '__main__':
    main()
