import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Total Bytes (Skipping 64 bytes)
bytes_x = [96, 128, 160, 192, 224, 256, 288, 320, 352, 384]

# Relative Percentage Improvement Data for SQ
ms_te3l_imp = [5.41, 5.50, 6.66, 7.27, 8.50, 6.83, 6.64, 5.84, 5.67, 5.15]
ms_cohere_imp = [6.66, 5.33, 5.74, 4.89, 5.18, 4.27, 3.73, 2.36, 1.36, 0.04]
db_te3l_imp = [5.11, 9.13, 6.99, 6.88, 6.89, 6.61, 6.33, 5.67, 4.33, 4.58]
db_cohere_imp = [8.41, 7.28, 9.34, 5.35, 4.02, 3.60, 2.44, 0.94, 0.07, -0.58]

# Absolute Recall Data [Uniform, Variable]
ms_te3l_uni = [45.67, 53.24, 58.30, 62.04, 65.08, 67.97, 69.86, 72.13, 73.55, 74.96]
ms_te3l_var = [48.14, 56.17, 62.18, 66.55, 70.61, 72.61, 74.50, 76.34, 77.72, 78.82]

ms_cohere_uni = [37.71, 46.71, 52.43, 57.65, 61.91, 65.63, 68.37, 71.20, 73.67, 76.12]
ms_cohere_var = [40.22, 49.20, 55.44, 60.47, 65.12, 68.43, 70.92, 72.88, 74.67, 76.15]

db_te3l_uni = [38.78, 46.42, 52.07, 56.38, 59.93, 62.79, 65.04, 67.38, 69.50, 70.68]
db_te3l_var = [40.76, 50.66, 55.71, 60.26, 64.06, 66.94, 69.16, 71.20, 72.51, 73.92]

db_cohere_uni = [32.00, 40.96, 46.88, 53.43, 57.53, 61.37, 64.81, 67.92, 70.51, 72.99]
db_cohere_var = [34.69, 43.94, 51.26, 56.29, 59.84, 63.58, 66.39, 68.56, 70.56, 72.57]

# Save directory configuration
save_dir = Path(__file__).resolve().parents[2] / 'NonUniform-Quantization' / 'figures'
save_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# CHART 1: SQ RELATIVE IMPROVEMENT (2x2 Grid)
# -------------------------------------------------------------------
fig1, axs1 = plt.subplots(2, 2, figsize=(14, 10))
fig1.suptitle('SQ Relative Improvement in Recall (%): Variable vs. Uniform Allocation', fontsize=16, fontweight='bold')

def plot_improvement(ax, data, title, color):
    ax.plot(bytes_x, data, marker='o', linestyle='-', color=color, linewidth=2, markersize=6)
    ax.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)
    
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel('Total Bytes', fontsize=11)
    ax.set_ylabel('Recall Improvement (%)', fontsize=11)
    ax.set_xticks(bytes_x)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Add 25% headroom to the y-axis to prevent text overlap with the top border
    y_min, y_max = min(0, min(data)), max(data)
    ax.set_ylim(y_min - 0.5, y_max + (y_max - y_min) * 0.25)
    
    # Label the maximum improvement peak
    max_idx = np.argmax(data)
    ax.annotate(f"{'+' if data[max_idx] > 0 else ''}{data[max_idx]:.2f}%", 
                xy=(bytes_x[max_idx], data[max_idx]),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=11, fontweight='bold', color=color)

plot_improvement(axs1[0, 0], ms_te3l_imp, 'MS Marco | text-embedding-3-large', '#1f77b4')
plot_improvement(axs1[0, 1], ms_cohere_imp, 'MS Marco | cohere-embed-4', '#ff7f0e')
plot_improvement(axs1[1, 0], db_te3l_imp, 'DBPedia | text-embedding-3-large', '#2ca02c')
plot_improvement(axs1[1, 1], db_cohere_imp, 'DBPedia | cohere-embed-4', '#d62728')

plt.tight_layout(rect=[0, 0, 1, 0.96])
imp_path = save_dir / 'sq_recall_improvement_grid.png'
plt.savefig(imp_path, dpi=300, bbox_inches='tight')
plt.close(fig1)
print(f"Saved SQ Improvement Grid to: {imp_path}")

# -------------------------------------------------------------------
# CHART 2: SQ ABSOLUTE RECALL COMPARISON (2x2 Grid)
# -------------------------------------------------------------------
fig2, axs2 = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle('SQ Recall Performance (%): Uniform vs. Variable Allocation', fontsize=16, fontweight='bold')

def plot_comparison(ax, uni_data, var_data, title):
    # Plot uniform baseline and variable allocations
    ax.plot(bytes_x, uni_data, marker='o', linestyle='--', color='gray', linewidth=2, markersize=6, label='Uniform Baseline')
    ax.plot(bytes_x, var_data, marker='^', linestyle='-', color='#1f77b4', linewidth=2, markersize=6, label='Variable (Greedy)')
    
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel('Total Bytes', fontsize=11)
    ax.set_ylabel('Recall (%)', fontsize=11)
    ax.set_xticks(bytes_x)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', fontsize=10)

plot_comparison(axs2[0, 0], ms_te3l_uni, ms_te3l_var, 'MS Marco | text-embedding-3-large')
plot_comparison(axs2[0, 1], ms_cohere_uni, ms_cohere_var, 'MS Marco | cohere-embed-4')
plot_comparison(axs2[1, 0], db_te3l_uni, db_te3l_var, 'DBPedia | text-embedding-3-large')
plot_comparison(axs2[1, 1], db_cohere_uni, db_cohere_var, 'DBPedia | cohere-embed-4')

plt.tight_layout(rect=[0, 0, 1, 0.96])
comp_path = save_dir / 'sq_recall_comparison_grid.png'
plt.savefig(comp_path, dpi=300, bbox_inches='tight')
plt.close(fig2)
print(f"Saved SQ Absolute Recall Comparison Grid to: {comp_path}")