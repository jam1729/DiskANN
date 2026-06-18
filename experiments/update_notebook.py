import json

cell0_source = """import matplotlib.pyplot as plt
import numpy as np
import parse_results_updated as parse_results

# --- Global Font Settings ---
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.titlesize': 20
})

dataset_names = ["MS Marco", "DBPedia", "Quora", "FiQA", "SciDocs", "SciFact"]

def get_line_plot_grid(model):
    grid = []
    # Row 0: PQ
    pq_row = []
    for ds in dataset_names:
        pq_row.append((ds, parse_results.get_greedy_data('PQ', ds, model)))
    grid.append(pq_row)
    # Row 1: SQ
    sq_row = []
    for ds in dataset_names:
        sq_row.append((ds, parse_results.get_greedy_data('SQ', ds, model)))
    grid.append(sq_row)
    return grid

models = [
    ('OAI text-embed-3-l', 'openai_text_large_3', parse_results.get_budgets('OAI text-embed-3-l')),
    ('Cohere embed-v4', 'cohere_v4', parse_results.get_budgets('Cohere embed-v4'))
]

def generate_line_plots(pearson=True):
    for model_label, model_key, budgets in models:
        grid_layout = get_line_plot_grid(model_label)
        row_labels = [f"PQ / {model_label}", f"SQ / {model_label}"]
        
        all_imps = []
        for row in grid_layout:
            for _, data in row:
                all_imps.extend(data['imps'])
        imp_ymin = min(all_imps) - 1 if all_imps else 0
        imp_ymax = max(all_imps) + 1 if all_imps else 100
        
        fig, axes = plt.subplots(2, 6, figsize=(36, 11))
        for r in range(2):
            for c in range(6):
                ax = axes[r, c]
                dataset_name, data = grid_layout[r][c]
                imps = data['imps']
                allocs = data['allocs']
                
                means = [np.mean(a) for a in allocs]
                stds = [np.std(a) for a in allocs]
                cvs = [s / m if m > 0 else 0 for s, m in zip(stds, means)]
                
                if pearson:
                    imps_arr = np.array(imps, dtype=float)
                    cvs_arr = np.array(cvs, dtype=float)
                    recall_skew_r = np.corrcoef(imps_arr, cvs_arr)[0, 1] if (np.std(imps_arr) > 0 and np.std(cvs_arr) > 0) else np.nan
                
                l1 = ax.plot(budgets, imps, marker='o', color='#1f77b4', linewidth=3, markersize=8, label='Recall $\\\\Delta$ (%)')
                if c == 0:
                    ax.set_ylabel('Recall $\\\\Delta$ (%)', color='#1f77b4', fontsize=18)
                else:
                    ax.set_ylabel('')
                ax.tick_params(axis='y', labelcolor='#1f77b4')
                ax.set_ylim(imp_ymin, imp_ymax)
                
                ax_twin = ax.twinx()
                l2 = ax_twin.plot(budgets, cvs, marker='X', color='#d62728', linestyle='--', linewidth=3, markersize=8, label='Norm Skew (CV)')
                if c == 5:
                    ax_twin.set_ylabel('Norm Skew (CV)', color='#d62728', fontsize=18)
                else:
                    ax_twin.set_ylabel('')
                ax_twin.tick_params(axis='y', labelcolor='#d62728')
                cv_ymax_local = max(cvs) * 1.1 if (cvs and max(cvs) > 0) else 1
                ax_twin.set_ylim(0, cv_ymax_local)
                
                if pearson:
                    ax.text(0.97, 0.97, f"r(Recall, Norm Skew)={recall_skew_r:.2f}", transform=ax.transAxes, ha='right', va='top', fontsize=11, bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.75, edgecolor='none'))
                
                if r == 0:
                    ax.set_title(dataset_name, pad=15)
                if c == 0:
                    ax.annotate(row_labels[r], xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 80, 0), xycoords=ax.yaxis.label, textcoords='offset points', size=18, ha='right', va='center', rotation=90)
                
                if r == 1:
                    ax.set_xlabel('Total Bytes Budget')
                    ax.set_xticks(budgets[::2])
                
                ax.grid(True, linestyle=':', alpha=0.7)
                
                if r == 1 and c == 2:
                    lns = l1 + l2
                    labs = [l.get_label() for l in lns]
                    ax.legend(lns, labs, loc='lower left', framealpha=0.9, edgecolor='black')
                    
        plt.tight_layout()
        fig.subplots_adjust(left=0.08, right=0.94, wspace=0.35, hspace=0.25)
        suffix = "" if pearson else "_no_pearson"
        filename = f"wide_normalized_skew_matrix_{model_key}{suffix}.pdf"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot generated successfully as {filename}")

generate_line_plots(pearson=True)
"""

cell1_source = """generate_line_plots(pearson=False)
"""

cell2_source = """import matplotlib.cm as cm
import matplotlib.colors as mcolors

for model_label, model_key, budgets in models:
    dataset_names = ["MS Marco", "DBPedia", "Quora", "FiQA", "SciDocs", "SciFact"]
    qm_rows = [
        (f"PQ / {model_label}", 'PQ'),
        (f"SQ / {model_label}", 'SQ')
    ]
    n_qm = len(qm_rows)
    n_budgets = len(budgets)
    
    all_allocs = []
    grid_data = []
    for row_label, quantizer in qm_rows:
        row_data = []
        for ds in dataset_names:
            data = parse_results.get_greedy_data(quantizer, ds, model_label)
            row_data.append(data)
            for alloc_list in data['allocs']:
                all_allocs.extend(alloc_list)
        grid_data.append(row_data)
        
    global_min = 0 
    global_max = 1.0
    if all_allocs:
        fractions = []
        for r_idx, (row_label, quantizer) in enumerate(qm_rows):
            for ds_i, ds in enumerate(dataset_names):
                for b_idx, b in enumerate(budgets):
                    alloc_arr = np.array(grid_data[r_idx][ds_i]['allocs'][b_idx], dtype=float)
                    fractions.extend(alloc_arr / b)
        global_min = min(fractions)
        global_max = max(fractions)
        
    cmap_hm = cm.YlOrRd
    norm_hm = mcolors.Normalize(vmin=global_min, vmax=global_max)
    
    fig_hm2, axes_hm2 = plt.subplots(n_qm, n_budgets, figsize=(32, 10), gridspec_kw={'wspace': 0.06, 'hspace': 0.45})
    
    for qm_i, (qm_label, quantizer) in enumerate(qm_rows):
        for budget_i, b in enumerate(budgets):
            if n_qm == 1:
                ax = axes_hm2[budget_i]
            else:
                ax = axes_hm2[qm_i, budget_i]
                
            matrix = np.array([
                grid_data[qm_i][ds_i]['allocs'][budget_i] for ds_i in range(6)
            ], dtype=float) / b
            
            ax.imshow(matrix, aspect='auto', cmap=cmap_hm, norm=norm_hm, interpolation='nearest')
            
            # White line to separate group 1 and group 2
            ax.axhline(2.5, color='white', linewidth=2.0)
            
            if qm_i == 0:
                ax.set_title(f'{b} B', fontsize=20)
                
            ax.set_xticks(range(8))
            if qm_i == n_qm - 1:
                ax.set_xticklabels([f'B{i+1}' for i in range(8)], fontsize=20, rotation=90, ha='center', va='top')
            else:
                ax.set_xticklabels([])
                
            if budget_i == 0:
                ax.set_yticks(range(6))
                ax.set_yticklabels(dataset_names, fontsize=16)
                ax.set_ylabel(qm_label, fontsize=22, labelpad=8)
            else:
                ax.set_yticks([])
                
    fig_hm2.subplots_adjust(right=0.87)
    cbar_ax2 = fig_hm2.add_axes([0.89, 0.12, 0.012, 0.76])
    sm2 = cm.ScalarMappable(cmap=cmap_hm, norm=norm_hm)
    sm2.set_array([])
    cbar2 = fig_hm2.colorbar(sm2, cax=cbar_ax2)
    cbar2.set_label('Fraction of total bit budget', fontsize=20)
    
    filename = f'wide_bit_allocations_heatmap_{model_key}.pdf'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot generated successfully as {filename}")
"""

cell3_source = """dataset_names = ["MS Marco", "DBPedia", "Quora", "FiQA", "SciDocs", "SciFact"]
quantizer_markers = {'PQ': 'o', 'SQ': 's'}
quantizer_linestyles = {'PQ': '-', 'SQ': ':'}
model_colors = {'OAI text-embed-3-l': '#1f77b4', 'Cohere embed-v4': '#d62728'}

for model_label, model_key, budgets in models:
    fig_uniform, axes_uniform = plt.subplots(1, 6, figsize=(36, 6), sharey=True)
    for ax, dataset in zip(axes_uniform, dataset_names):
        for quantizer in ['PQ', 'SQ']:
            uniform_recalls = parse_results.get_uniform_recalls(quantizer, dataset, model_label)
            ax.plot(budgets, uniform_recalls, marker=quantizer_markers[quantizer], linestyle=quantizer_linestyles[quantizer], linewidth=2.5, markersize=7, color=model_colors[model_label], label=f'{model_label} / {quantizer}')
        ax.set_title(dataset, fontsize=30)
        ax.set_xlabel('Bit Budget', fontsize=24)
        ax.set_xticks(budgets)
        ax.tick_params(axis='x', labelsize=18)
        ax.tick_params(axis='y', labelsize=18)
        ax.set_xticklabels(budgets, rotation=90, ha='center', va='top')
        ax.grid(True, linestyle=':', alpha=0.7)
    axes_uniform[0].set_ylabel('Recall (%)', fontsize=24)
    axes_uniform[5].legend(loc='best', framealpha=0.9, edgecolor='black')
    plt.tight_layout()
    filename = f'uniform_bit_allocation_recall_{model_key}.pdf'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f'Plot generated successfully as {filename}')
"""

# Format cells
def make_cell(source_code):
    return [line + "\n" for line in source_code.split("\n")[:-1]]

with open('/home/jam1729/DiskANN/experiments/figures_updated.ipynb', 'r') as f:
    nb = json.load(f)

# Replace code in the first 4 code cells
code_cells = [cell for cell in nb['cells'] if cell['cell_type'] == 'code']
if len(code_cells) >= 4:
    code_cells[0]['source'] = make_cell(cell0_source)
    code_cells[1]['source'] = make_cell(cell1_source)
    code_cells[2]['source'] = make_cell(cell2_source)
    code_cells[3]['source'] = make_cell(cell3_source)

# Clear outputs so the file isn't huge and outputs will be re-generated cleanly
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []

with open('/home/jam1729/DiskANN/experiments/figures_updated.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
