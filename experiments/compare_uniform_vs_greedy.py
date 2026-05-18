#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

# Data
bytes_values = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]

uniform_recall = [47.0814, 60.3447, 68.3855, 73.4857, 77.0812, 79.5797, 81.6388, 82.9589, 84.1393, 85.202, 86.2391]

greedy_recall = [47.6166, 64.0350, 71.6271, 75.9834, 79.0106, 81.3006, 82.9772, 84.3635, 85.4739, 86.4503, 87.2676]

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

# Plot both lines
ax.plot(bytes_values, uniform_recall, marker='o', linewidth=2.5, markersize=8, label='Uniform', color='#1f77b4')
ax.plot(bytes_values, greedy_recall, marker='s', linewidth=2.5, markersize=8, label='Greedy', color='#ff7f0e')

# Add some styling
ax.set_xlabel('Total PQ Bytes', fontsize=13, fontweight='bold')
ax.set_ylabel('Recall (%)', fontsize=13, fontweight='bold')
ax.set_title('Uniform vs Greedy PQ Allocation: Recall Performance', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=12, loc='lower right')

# Set x-axis ticks to show all byte values
ax.set_xticks(bytes_values)
ax.set_xticklabels(bytes_values, rotation=45)

# Set y-axis limits for better visibility
ax.set_ylim([45, 88])

# Tight layout
plt.tight_layout()

# Save the figure
output_path = '/home/jam1729/DiskANN/experiments/uniform_vs_greedy.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Chart saved to {output_path}")

# Also print the difference at each point
print("\nRecall Difference (Greedy - Uniform):")
print("Bytes\tGreedy\tUniform\tDifference")
print("-" * 45)
for i, b in enumerate(bytes_values):
    diff = greedy_recall[i] - uniform_recall[i]
    print(f"{b}\t{greedy_recall[i]:.4f}\t{uniform_recall[i]:.4f}\t{diff:+.4f}")
