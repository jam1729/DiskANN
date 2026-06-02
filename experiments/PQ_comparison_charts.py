from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Total Bytes (Skipping 64 bytes)
bytes_x = [96, 128, 160, 192, 224, 256, 288, 320, 352, 384]

# Relative Percentage Improvement Data
ms_te3l_imp = [6.13, 4.74, 3.39, 2.50, 2.16, 1.64, 1.69, 1.58, 1.47, 1.19]
ms_cohere_imp = [0.51, 0.57, 0.68, 0.67, 0.80, 0.30, 0.56, 0.56, 0.71, 0.00]
db_te3l_imp = [8.09, 5.00, 3.87, 2.62, 2.43, 2.05, 2.37, 2.05, 1.69, 1.86]
db_cohere_imp = [1.39, 0.49, 1.21, 0.53, 0.42, 0.18, 0.82, 0.52, 1.13, 0.09]

# Absolute Recall Data [Uniform, Variable]
ms_te3l_uni = [60.34, 68.39, 73.49, 77.08, 79.58, 81.64, 82.96, 84.14, 85.20, 86.24]
ms_te3l_var = [64.04, 71.63, 75.98, 79.01, 81.30, 82.98, 84.36, 85.47, 86.45, 87.27]

ms_cohere_uni = [64.34, 69.61, 73.01, 76.07, 78.50, 80.91, 82.63, 84.46, 85.77, 87.69]
ms_cohere_var = [64.67, 70.01, 73.51, 76.58, 79.13, 81.15, 83.09, 84.93, 86.38, 87.69]

db_te3l_uni = [54.12, 63.86, 69.70, 73.92, 76.67, 78.96, 80.18, 81.61, 82.94, 83.74]
db_te3l_var = [58.50, 67.05, 72.40, 75.86, 78.53, 80.58, 82.08, 83.28, 84.34, 85.30]

db_cohere_uni = [59.59, 65.83, 69.52, 73.18, 75.93, 78.62, 80.38, 82.43, 83.73, 85.94]
db_cohere_var = [60.42, 66.15, 70.36, 73.57, 76.25, 78.76, 81.04, 82.86, 84.68, 86.02]

save_dir = Path(__file__).resolve().parents[2] / 'NonUniform-Quantization' / 'figures'
save_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# CHART 1: RELATIVE IMPROVEMENT (2x2 Grid)
# -------------------------------------------------------------------
fig1, axs1 = plt.subplots(2, 2, figsize=(14, 10))
fig1.suptitle('Relative Improvement in Recall (%): Variable vs. Uniform Allocation', fontsize=16, fontweight='bold')

def plot_improvement(ax, data, title, color):
    ax.plot(bytes_x, data, marker='o', linestyle='-', color=color, linewidth=2, markersize=6)
    ax.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)
    
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel('Total Bytes', fontsize=11)
    ax.set_ylabel('Recall Improvement (%)', fontsize=11)
    ax.set_xticks(bytes_x)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Add 20% headroom to the y-axis to prevent text overlap with the top border
    y_min, y_max = min(0, min(data)), max(data)
    ax.set_ylim(y_min - 0.2, y_max + (y_max - y_min) * 0.25)
    
    # Label the maximum improvement peak
    max_idx = np.argmax(data)
    ax.annotate(f"+{data[max_idx]:.2f}%", 
                xy=(bytes_x[max_idx], data[max_idx]),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=11, fontweight='bold', color=color)

plot_improvement(axs1[0, 0], ms_te3l_imp, 'MS Marco | text-embedding-3-large', '#1f77b4')
plot_improvement(axs1[0, 1], ms_cohere_imp, 'MS Marco | cohere-embed-4', '#ff7f0e')
plot_improvement(axs1[1, 0], db_te3l_imp, 'DBPedia | text-embedding-3-large', '#2ca02c')
plot_improvement(axs1[1, 1], db_cohere_imp, 'DBPedia | cohere-embed-4', '#d62728')

plt.tight_layout(rect=[0, 0, 1, 0.96])
imp_path = save_dir / 'pq_recall_improvement_grid.png'
plt.savefig(imp_path, dpi=300, bbox_inches='tight')
plt.close(fig1)
print(f"Saved Improvement Grid to: {imp_path}")


# -------------------------------------------------------------------
# CHART 2: ABSOLUTE RECALL COMPARISON (2x2 Grid)
# -------------------------------------------------------------------
fig2, axs2 = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle('Recall Performance (%): Uniform vs. Variable Allocation', fontsize=16, fontweight='bold')

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
comp_path = save_dir / 'pq_recall_comparison_grid.png'
plt.savefig(comp_path, dpi=300, bbox_inches='tight')
plt.close(fig2)
print(f"Saved Absolute Recall Comparison Grid to: {comp_path}")