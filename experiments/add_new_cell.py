
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
        bpd_array = [b * 8 / dim for b in budgets]
        
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
        for row in grid_layout:
            for _, data, _, _ in row:
                all_imps.extend(data['imps'])
        imp_ymin = min(all_imps) - 1 if all_imps else 0
        imp_ymax = max(all_imps) + 1 if all_imps else 100
        
        inner_gs = gridspec.GridSpecFromSubplotSpec(2, 3, subplot_spec=outer_gs[block_i], hspace=0.30, wspace=0.35)
        
        for r in range(2):
            for c in range(3):
                ax = fig.add_subplot(inner_gs[r, c])
                dataset_name, data, uni, var = grid_layout[r][c]
                imps = data['imps']
                
                l1 = ax.plot(bpd_array, imps, marker='o', color='#1f77b4', linewidth=3, markersize=8, label='Recall $\\Delta$ (%)')
                if c == 0:
                    ax.set_ylabel('Recall $\\Delta$ (%)', color='#1f77b4', fontsize=18)
                else:
                    ax.set_ylabel('')
                ax.tick_params(axis='y', labelcolor='#1f77b4')
                ax.set_ylim(imp_ymin, imp_ymax)
                
                ax_twin = ax.twinx()
                l2 = ax_twin.plot(bpd_array, uni, marker='^', color='#ff7f0e', linestyle='--', linewidth=2, markersize=6, alpha=0.6, label='Uniform Recall')
                l3 = ax_twin.plot(bpd_array, var, marker='v', color='#2ca02c', linestyle='--', linewidth=2, markersize=6, alpha=0.6, label='Variable Recall')
                
                if c == 2:
                    ax_twin.set_ylabel('Absolute Recall@100 (%)', color='#555555', fontsize=18)
                else:
                    ax_twin.set_ylabel('')
                ax_twin.tick_params(axis='y', labelcolor='#555555')
                
                all_recalls = uni + var
                recall_ymin = min(all_recalls) - 5 if all_recalls else 0
                recall_ymax = max(all_recalls) + 5 if all_recalls else 100
                ax_twin.set_ylim(recall_ymin, recall_ymax)
                
                ax.set_title(dataset_name.replace('DBPedia', 'DBpedia'), pad=15)
                
                if c == 0:
                    row_label = f"{quantizer} / {display_model}"
                    ax.annotate(row_label, xy=(-0.35, 0.5), xycoords='axes fraction', size=18, ha='right', va='center', rotation=90)
                
                ax.set_xticks(bpd_array)
                if r == 1:
                    ax.set_xticklabels([f"{x:.2f}" for x in bpd_array], rotation=90, ha='center', va='top')
                else:
                    ax.set_xticklabels([])
                
                if block_i == 1 and r == 0 and c == 1:
                    lns = l1 + l2 + l3
                    labs = [l.get_label() for l in lns]
                    ax.legend(lns, labs, loc='lower left', framealpha=0.9, edgecolor='black')
                
                ax.grid(True, linestyle=':', alpha=0.7)
                
    fig.text(0.5, 0.08, 'Bits per Dimension (bpd)', ha='center', va='center', fontsize=22)
    plt.subplots_adjust(bottom=0.12, left=0.10, right=0.92)
    filename = "wide_recall_delta_with_absolute_recalls_combined.pdf"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot generated successfully as {filename}")

generate_recall_comparison_plots()
