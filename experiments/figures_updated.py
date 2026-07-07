# CELL 0
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import parse_results_updated as parse_results

# --- Global Font Settings ---
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.titlesize': 20,
    'pdf.fonttype': 42
})

dataset_group1 = ["MS Marco", "DBPedia", "Quora"]
dataset_group2 = ["FiQA", "SciDocs", "SciFact"]
dataset_names = dataset_group1 + dataset_group2

models_info = [
    ('OAI text-embed-3-l', 'OAI te3-l', 'openai_text_large_3', parse_results.get_budgets('OAI text-embed-3-l'), 3072),
    ('Cohere embed-v4', 'cohere-e4', 'cohere_v4', parse_results.get_budgets('Cohere embed-v4'), 1536)
]

def generate_line_plots(pearson=True, plot_skew=True):
    fig = plt.figure(figsize=(22, 28))
    outer_gs = gridspec.GridSpec(4, 1, hspace=0.35)
    
    blocks = [
        (models_info[0], 'PQ'),
        (models_info[0], 'SQ'),
        (models_info[1], 'PQ'),
        (models_info[1], 'SQ'),
    ]
    
    for block_i, (model_data, quantizer) in enumerate(blocks):
        orig_model, display_model, model_key, budgets, dim = model_data
        bpd_array = [b * 8 / dim for b in budgets]
        
        grid_layout = []
        row = []
        for ds in dataset_group1:
            row.append((ds, parse_results.get_greedy_data(quantizer, ds, orig_model)))
        grid_layout.append(row)
        row = []
        for ds in dataset_group2:
            row.append((ds, parse_results.get_greedy_data(quantizer, ds, orig_model)))
        grid_layout.append(row)
        
        all_imps = []
        for row in grid_layout:
            for _, data in row:
                all_imps.extend(data['imps'])
        imp_ymin = min(all_imps) - 1 if all_imps else 0
        imp_ymax = max(all_imps) + 1 if all_imps else 100
        
        inner_gs = gridspec.GridSpecFromSubplotSpec(2, 3, subplot_spec=outer_gs[block_i], hspace=0.30, wspace=0.35)
        
        for r in range(2):
            for c in range(3):
                ax = fig.add_subplot(inner_gs[r, c])
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
                
                l1 = ax.plot(bpd_array, imps, marker='o', color='#1f77b4', linewidth=3, markersize=8, label='Recall $\\Delta$ (%)')
                if c == 0:
                    ax.set_ylabel('Recall $\\Delta$ (%)', color='#1f77b4', fontsize=18)
                else:
                    ax.set_ylabel('')
                ax.tick_params(axis='y', labelcolor='#1f77b4')
                ax.set_ylim(imp_ymin, imp_ymax)
                
                if plot_skew:
                    ax_twin = ax.twinx()
                    l2 = ax_twin.plot(bpd_array, cvs, marker='X', color='#d62728', linestyle='--', linewidth=3, markersize=8, label='Norm Skew (CV)')
                    if c == 2:
                        ax_twin.set_ylabel('Norm Skew (CV)', color='#d62728', fontsize=18)
                    else:
                        ax_twin.set_ylabel('')
                    ax_twin.tick_params(axis='y', labelcolor='#d62728')
                    cv_ymax_local = max(cvs) * 1.1 if (cvs and max(cvs) > 0) else 1
                    ax_twin.set_ylim(0, cv_ymax_local)
                
                if pearson and plot_skew:
                    ax.text(0.97, 0.97, f"r(Recall, Norm Skew)={recall_skew_r:.2f}", transform=ax.transAxes, ha='right', va='top', fontsize=11, bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.75, edgecolor='none'))
                
                ax.set_title(dataset_name.replace('DBPedia', 'DBpedia'), pad=15)
                
                if r == 0 and c == 0:
                    row_label = f"{quantizer} / {display_model}"
                    ax.annotate(row_label, xy=(-0.35, -0.15), xycoords='axes fraction', size=18, ha='right', va='center', rotation=90)
                
                ax.set_xticks(bpd_array)
                if r == 1:
                    ax.set_xticklabels([f"{x:.2f}" for x in bpd_array], rotation=90, ha='center', va='top')
                else:
                    ax.set_xticklabels([])
                
                # Legend logic: SQ OAI (block 1), row 0, col 1 at bottom left
                if block_i == 1 and r == 0 and c == 1:
                    lns = l1
                    if plot_skew:
                        lns += l2
                    labs = [l.get_label() for l in lns]
                    ax.legend(lns, labs, loc='lower left', framealpha=0.9, edgecolor='black')
                
                ax.grid(True, linestyle=':', alpha=0.7)
                
    fig.text(0.5, 0.08, 'Bits per Dimension (bpd)', ha='center', va='center', fontsize=22)
    plt.subplots_adjust(bottom=0.12, left=0.10, right=0.92)
    suffix = "" if pearson else "_no_pearson"
    if not plot_skew:
        suffix += "_no_skew"
    filename = f"wide_normalized_skew_matrix_combined{suffix}.pdf"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot generated successfully as {filename}")

generate_line_plots(pearson=True, plot_skew=False)



# CELL 1
generate_line_plots(pearson=False, plot_skew=False)




# CELL 2
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# First compute the absolute global min/max across ALL models and ALL quantizers
global_fractions = []
for orig_model, display_model, model_key, budgets, dim in models_info:
    for quantizer in ['PQ', 'SQ']:
        for ds in dataset_names:
            data = parse_results.get_greedy_data(quantizer, ds, orig_model)
            for b_idx, b in enumerate(budgets):
                alloc_arr = np.array(data['allocs'][b_idx], dtype=float)
                global_fractions.extend(alloc_arr / b)

global_min = min(global_fractions) if global_fractions else 0
global_max = max(global_fractions) if global_fractions else 1.0

cmap_hm = cm.YlOrRd
norm_hm = mcolors.Normalize(vmin=global_min, vmax=global_max)

qm_rows = []
for orig_model, display_model, model_key, budgets, dim in models_info:
    qm_rows.extend([
        (f"PQ / {display_model}", 'PQ', orig_model, budgets, dim),
        (f"SQ / {display_model}", 'SQ', orig_model, budgets, dim)
    ])

n_qm = len(qm_rows)
n_budgets = len(models_info[0][3])

fig_hm2, axes_hm2 = plt.subplots(n_qm, n_budgets, figsize=(32, 20), gridspec_kw={'wspace': 0.06, 'hspace': 0.45})

for qm_i, (qm_label, quantizer, orig_model, budgets, dim) in enumerate(qm_rows):
    grid_data = []
    for ds in dataset_names:
        grid_data.append(parse_results.get_greedy_data(quantizer, ds, orig_model))
        
    for budget_i, b in enumerate(budgets):
        ax = axes_hm2[qm_i, budget_i]
        bpd = b * 8 / dim
            
        matrix = np.array([
            grid_data[ds_i]['allocs'][budget_i] for ds_i in range(6)
        ], dtype=float) / b
        
        ax.imshow(matrix, aspect='auto', cmap=cmap_hm, norm=norm_hm, interpolation='nearest')
        
        for y_line in [0.5, 1.5, 3.5, 4.5]:
            ax.axhline(y_line, color='white', linewidth=1.0)
        ax.axhline(2.5, color='white', linewidth=3.0)
        
        ax.set_title(f'{bpd:.2f} bpd', fontsize=20)
            
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

filename = 'wide_bit_allocations_heatmap_combined.pdf'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Plot generated successfully as {filename}")



# CELL 3
dataset_grid = [dataset_group1, dataset_group2]
quantizer_markers = {'PQ': 'o', 'SQ': 's'}
quantizer_linestyles = {'PQ': '-', 'SQ': ':'}
display_colors = {'OAI te3-l': '#1f77b4', 'cohere-e4': '#d62728'}

fig_uniform, axes_uniform = plt.subplots(2, 3, figsize=(21, 12), sharey=True)
for r in range(2):
    for c in range(3):
        ax = axes_uniform[r, c]
        dataset = dataset_grid[r][c]
        
        all_bpds = set()
        for orig_model, display_model, model_key, budgets, dim in models_info:
            bpd_array = [b * 8 / dim for b in budgets][1:]
            all_bpds.update(bpd_array)
            for quantizer in ['PQ', 'SQ']:
                uniform_recalls = parse_results.get_uniform_recalls(quantizer, dataset, orig_model)[1:]
                ax.plot(bpd_array, uniform_recalls, marker=quantizer_markers[quantizer], linestyle=quantizer_linestyles[quantizer], linewidth=2.5, markersize=7, color=display_colors[display_model], label=f'{display_model} / {quantizer}')
        
        ax.set_title(dataset.replace('DBPedia', 'DBpedia'), fontsize=30)
        
        if r == 1:
            ax.set_xlabel('Bits per Dimension (bpd)', fontsize=24)
            
        sorted_bpds = sorted(list(all_bpds))
        ax.set_xticks(sorted_bpds[::2])
        ax.tick_params(axis='x', labelsize=18)
        ax.tick_params(axis='y', labelsize=18)
        ax.set_xticklabels([f"{x:.2f}" for x in sorted_bpds[::2]], rotation=90, ha='center', va='top')
        ax.grid(True, linestyle=':', alpha=0.7)
        
        if c == 0:
            ax.set_ylabel('Recall (%)', fontsize=24)
        if r == 1 and c == 2:
            ax.legend(loc='best', framealpha=0.9, edgecolor='black', fontsize=12)
            
plt.tight_layout()
filename = 'uniform_bit_allocation_recall_combined.pdf'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f'Plot generated successfully as {filename}')



# CELL 4
def generate_recall_comparison_plots():
    fig = plt.figure(figsize=(22, 28))
    outer_gs = gridspec.GridSpec(4, 1, hspace=0.35)
    
    blocks = [
        (models_info[0], 'PQ'),
        (models_info[0], 'SQ'),
        (models_info[1], 'PQ'),
        (models_info[1], 'SQ'),
    ]
    
    for block_i, (model_data, quantizer) in enumerate(blocks):
        orig_model, display_model, model_key, budgets, dim = model_data
        bpd_array = [b * 8 / dim for b in budgets][1:]
        
        grid_layout = []
        row = []
        for ds in dataset_group1:
            data = parse_results.get_greedy_data(quantizer, ds, orig_model)
            uni = parse_results.get_uniform_recalls(quantizer, ds, orig_model)
            var = parse_results.get_variable_recalls(quantizer, ds, orig_model)
            row.append((ds, data, uni, var))
        grid_layout.append(row)
        row = []
        for ds in dataset_group2:
            data = parse_results.get_greedy_data(quantizer, ds, orig_model)
            uni = parse_results.get_uniform_recalls(quantizer, ds, orig_model)
            var = parse_results.get_variable_recalls(quantizer, ds, orig_model)
            row.append((ds, data, uni, var))
        grid_layout.append(row)
        
        all_imps = []
        all_group_recalls = []
        for row in grid_layout:
            for _, data, uni, var in row:
                all_imps.extend(data['imps'][1:])
                all_group_recalls.extend(uni[1:])
                all_group_recalls.extend(var[1:])
                
        imp_ymin = min(all_imps) - 1 if all_imps else 0
        imp_ymax = max(all_imps) + 1 if all_imps else 100
        
        imp_ymin = min(all_imps) - 1 if all_imps else 0
        imp_ymax = max(all_imps) + 1 if all_imps else 100
        
        recall_ymin = min(all_group_recalls) - 5 if all_group_recalls else 0
        recall_ymax = max(all_group_recalls) + 5 if all_group_recalls else 100
        
        inner_gs = gridspec.GridSpecFromSubplotSpec(2, 3, subplot_spec=outer_gs[block_i], hspace=0.30, wspace=0.35)
        
        for r in range(2):
            for c in range(3):
                ax = fig.add_subplot(inner_gs[r, c])
                dataset_name, data, uni, var = grid_layout[r][c]
                imps = data['imps'][1:]
                uni = uni[1:]
                var = var[1:]
                
                l1 = ax.plot(bpd_array, imps, marker='o', color='#1f77b4', linewidth=3, markersize=8, label='Recall $\\Delta$ (%)')
                if r == 0 and c == 0:
                    ax.set_ylabel('Recall $\\Delta$ (%)', color='#1f77b4', fontsize=18)
                    ax.yaxis.set_label_coords(-0.13, -0.15)
                else:
                    ax.set_ylabel('')
                ax.tick_params(axis='y', labelcolor='#1f77b4')
                ax.set_ylim(imp_ymin, imp_ymax)
                
                ax_twin = ax.twinx()
                l2 = ax_twin.plot(bpd_array, uni, marker='^', color='#999999', linestyle='--', linewidth=2, markersize=6, alpha=0.7, label='Uniform Recall')
                l3 = ax_twin.plot(bpd_array, var, marker='v', color='#d62728', linestyle='--', linewidth=2, markersize=6, alpha=0.5, label='Variable Recall')
                
                if r == 0 and c == 2:
                    ax_twin.set_ylabel('Absolute Recall@100 (%)', color='#555555', fontsize=18)
                    ax_twin.yaxis.set_label_coords(1.13, -0.15)
                else:
                    ax_twin.set_ylabel('')
                ax_twin.tick_params(axis='y', labelcolor='#555555')
                
                ax_twin.set_ylim(recall_ymin, recall_ymax)
                
                ax.set_title(dataset_name.replace('DBPedia', 'DBpedia'), pad=15)
                
                if r == 0 and c == 0:
                    row_label = f"{quantizer} / {display_model}"
                    ax.annotate(row_label, xy=(-0.35, -0.15), xycoords='axes fraction', size=18, ha='right', va='center', rotation=90)
                
                ax.set_xticks(bpd_array)
                if r == 1:
                    ax.set_xticklabels([f"{x:.2f}" for x in bpd_array], rotation=90, ha='center', va='top')
                else:
                    ax.set_xticklabels([])
                
                if block_i == 3 and r == 0 and c == 2:
                    lns = l1 + l2 + l3
                    labs = [l.get_label() for l in lns]
                    ax.legend(lns, labs, loc='upper left', framealpha=0.9, edgecolor='black', fontsize=10)
                
                ax.grid(True, linestyle=':', alpha=0.7)
                
    fig.text(0.5, 0.08, 'Bits per Dimension (bpd)', ha='center', va='center', fontsize=22)
    plt.subplots_adjust(bottom=0.12, left=0.10, right=0.92)
    filename = "wide_recall_delta_with_absolute_recalls_combined.pdf"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot generated successfully as {filename}")

generate_recall_comparison_plots()
