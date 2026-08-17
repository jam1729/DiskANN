import matplotlib.pyplot as plt

# Data arrays for standard 32-byte increments
bytes_standard = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]

recall_uniform = [60.021, 67.256, 72.166, 75.378, 77.761, 79.843, 81.381, 82.574, 83.715, 84.755, 85.905]
recall_kmeans_exact = [62.608, 68.400, 72.283, 75.436, 79.339, 81.881, 83.199, 84.488, 85.543, 86.373, 86.961]
recall_kmeans_tau = [62.759, 69.453, 74.004, 77.459, 79.932, 81.671, 83.226, 84.585, 85.687, 86.649, 87.559]

# Exhaustive max recall per 8-byte increment extracted from Greedy logs
bytes_greedy = list(range(64, 392, 8))
recall_greedy = [
    60.120, 63.659, 66.212, 68.076, 69.758, 71.035, 72.491, 73.533, 74.743, 
    75.674, 76.512, 77.211, 77.747, 78.510, 78.979, 79.600, 80.271, 80.767, 
    81.212, 81.663, 82.183, 82.456, 83.001, 83.362, 83.646, 83.931, 84.332, 
    84.695, 84.941, 85.217, 85.596, 85.841, 86.097, 86.228, 86.534, 86.796, 
    87.002, 87.204, 87.369, 87.706, 87.881
]

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(bytes_standard, recall_kmeans_tau, marker='o', label='k-means-tau-weighted PQ', linewidth=2)
plt.plot(bytes_standard, recall_kmeans_exact, marker='v', label='k-means-exact PQ', linewidth=2)
# plt.plot(bytes_greedy, recall_greedy, marker='s', markersize=4, label='Greedy PQ (Best)', linewidth=2)
# plt.plot(bytes_standard, recall_uniform, marker='^', label='Uniform PQ', linewidth=2, linestyle='--')

# Formatting
plt.title('SCIDOCS OpenAI Embeddings: PQ Bit Allocation Strategies', fontsize=14, pad=15)
plt.xlabel('Byte Budget', fontsize=12)
plt.ylabel('Recall@100', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(loc='lower right', fontsize=11)
plt.xlim(60, 390)

plt.tight_layout()
plt.savefig('scidocs_pq_recall_just_kmeans.pdf', format='pdf', bbox_inches='tight')