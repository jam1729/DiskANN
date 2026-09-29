#!/usr/bin/env python3
"""
Plotting script for PQ + OpenAI text-embedding-3-large alone:
1. Line Plot (Recall Delta vs Bits per Dimension)
2. Bit Allocations Heatmap
3. Dimension Variance Plot (Rolling Mean Variance, Window=128)

Follows the exact layout, styling, and logic from figures_updated.ipynb and plot_rolling_variance.py.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Tuple, List, Dict, Any
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# --- Configure Matplotlib ---
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
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

# ==============================================================================
# 1. PATHS & DATA CONFIGURATION
# ==============================================================================
RUNS_BASE_DIR = Path('/home/sreeramjiks/runs/results')
EMBEDDINGS_DIR = Path('/home/sreeramjiks/data/embeddings')
OUTPUT_DIR = Path('/home/sreeramjiks/DiskANN/experiments/plotting')

DATASETS_GROUP_1 = {
    'MS Marco': 'msmarco_500k',
    'DBPedia': 'dbpedia_entity_500k',
    'Quora': 'quora_500k'
}

DATASETS_GROUP_2 = {
    'FiQA': 'fiqa',
    'SciDocs': 'scidocs',
    'SciFact': 'scifact'
}

ALL_DATASETS = {**DATASETS_GROUP_1, **DATASETS_GROUP_2}
DATASET_NAMES = list(DATASETS_GROUP_1.keys()) + list(DATASETS_GROUP_2.keys())

MODEL_ORIG = 'OAI text-embed-3-l'
MODEL_DISPLAY = 'OAI te3-l'
MODEL_KEY = 'openai_text_large_3'
MODEL_DIM = 3072
QUANTIZER = 'PQ'

def get_budgets(model=MODEL_ORIG):
    return [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]

def parse_uniform(file_path, model=MODEL_ORIG):
    budgets = get_budgets(model)
    expected_lines = 11
    
    lines = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)
            
    assert len(lines) == expected_lines, f"Expected {expected_lines} non-empty lines in {file_path}, got {len(lines)}"
    
    data = {}
    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Expected comma separated values in {file_path}, got {line}"
        b = int(parts[0])
        recall = float(parts[1])
        data[b] = recall
        
    for b in budgets:
        assert b in data, f"Budget {b} not found in {file_path}"
        
    return data

def parse_variable(file_path, model=MODEL_ORIG):
    lines_parsed = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                lines_parsed.append(line)
                
    parsed_entries = []
    for line in lines_parsed:
        alloc_match = re.search(r'alloc=\[(.*?)\]', line)
        bytes_match = re.search(r'bytes=(\d+)', line)
        recall_match = re.search(r'recall=([\d.]+)', line)
        
        if alloc_match and bytes_match and recall_match:
            alloc = [int(x.strip()) for x in alloc_match.group(1).split(',')]
            b = int(bytes_match.group(1))
            recall = float(recall_match.group(1))
            parsed_entries.append({'alloc': alloc, 'bytes': b, 'recall': recall})
            
    assert len(parsed_entries) >= 320, f"Expected at least 320 valid lines, got {len(parsed_entries)} in {file_path}"
        
    by_bytes = {}
    for entry in parsed_entries:
        b = entry['bytes']
        if b not in by_bytes:
            by_bytes[b] = []
        by_bytes[b].append(entry)
        
    best_by_bytes = {}
    budgets = get_budgets(model)
    for b in budgets:
        if b in by_bytes:
            best_entry = max(by_bytes[b], key=lambda x: (x['recall'], x['alloc']))
            best_by_bytes[b] = (best_entry['alloc'], best_entry['recall'])
        
    return best_by_bytes

def get_greedy_data(quantizer=QUANTIZER, dataset='MS Marco', model=MODEL_ORIG):
    dir_path = RUNS_BASE_DIR / quantizer.lower() / ALL_DATASETS[dataset] / MODEL_KEY
    uni_data = parse_uniform(dir_path / 'uniform.txt', model)
    var_data = parse_variable(dir_path / 'variable.txt', model)
    
    budgets = get_budgets(model)
    imps = []
    allocs = []
    
    for b in budgets:
        recall_uni = uni_data[b]
        alloc, recall_var = var_data[b]
        imp = ((recall_var - recall_uni) / recall_uni) * 100
        imps.append(imp)
        allocs.append(alloc)
        
    return {'imps': imps, 'allocs': allocs}

def get_uniform_recalls(quantizer=QUANTIZER, dataset='MS Marco', model=MODEL_ORIG):
    dir_path = RUNS_BASE_DIR / quantizer.lower() / ALL_DATASETS[dataset] / MODEL_KEY
    uni_data = parse_uniform(dir_path / 'uniform.txt', model)
    budgets = get_budgets(model)
    return [uni_data[b] for b in budgets]

def get_variable_recalls(quantizer=QUANTIZER, dataset='MS Marco', model=MODEL_ORIG):
    dir_path = RUNS_BASE_DIR / quantizer.lower() / ALL_DATASETS[dataset] / MODEL_KEY
    var_data = parse_variable(dir_path / 'variable.txt', model)
    budgets = get_budgets(model)
    return [var_data[b][1] for b in budgets]

## ==============================================================================
# 2. PLOT 1: LINE PLOT (Recall Delta vs bpd for PQ + OpenAI)
# ==============================================================================
def generate_line_plots(pearson=False, plot_skew=False, output_filename=None):
    """Generate 2x3 line plot for PQ + OpenAI text-embed-3-l."""
    budgets = get_budgets(MODEL_ORIG)
    bpd_array = [b * 8 / MODEL_DIM for b in budgets]
    
    fig = plt.figure(figsize=(22, 7.5))
    inner_gs = gridspec.GridSpec(2, 3, hspace=0.35, wspace=0.35)
    
    grid_layout = []
    row = []
    for ds in DATASETS_GROUP_1.keys():
        row.append((ds, get_greedy_data(QUANTIZER, ds, MODEL_ORIG)))
    grid_layout.append(row)
    
    row = []
    for ds in DATASETS_GROUP_2.keys():
        row.append((ds, get_greedy_data(QUANTIZER, ds, MODEL_ORIG)))
    grid_layout.append(row)
    
    all_imps = []
    for row_data in grid_layout:
        for _, data in row_data:
            all_imps.extend(data['imps'])
    imp_ymin = min(all_imps) - 1 if all_imps else 0
    imp_ymax = max(all_imps) + 1 if all_imps else 100
    
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
                    ax_twin.set_ylabel('Norm Skew (CV)', color='#d62728', fontsize=18, labelpad=12)
                else:
                    ax_twin.set_ylabel('')
                ax_twin.tick_params(axis='y', labelcolor='#d62728')
                cv_ymax_local = max(cvs) * 1.1 if (cvs and max(cvs) > 0) else 1
                ax_twin.set_ylim(0, cv_ymax_local)
            
            if pearson and plot_skew:
                ax.text(0.97, 0.97, f"r(Recall, Norm Skew)={recall_skew_r:.2f}", transform=ax.transAxes, ha='right', va='top', fontsize=11, bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.75, edgecolor='none'))
            
            ax.set_title(dataset_name.replace('DBPedia', 'DBpedia'), pad=15)
            
            if r == 0 and c == 0:
                row_label = f"{QUANTIZER} / {MODEL_DISPLAY}"
                ax.annotate(row_label, xy=(-0.24, -0.15), xycoords='axes fraction', size=18, ha='right', va='center', rotation=90)
            
            ax.set_xticks(bpd_array)
            if r == 1:
                ax.set_xticklabels([f"{x:.2f}" for x in bpd_array], rotation=90, ha='center', va='top')
            else:
                ax.set_xticklabels([])
            
            # Show legend on row 0, col 1
            if r == 0 and c == 1:
                lns = l1
                if plot_skew:
                    lns += l2
                labs = [l.get_label() for l in lns]
                ax.legend(lns, labs, loc='lower left', framealpha=0.9, edgecolor='black')
            
            ax.grid(True, linestyle=':', alpha=0.7)
            
    fig.text(0.5, 0.01, 'Bits per Dimension (bpd)', ha='center', va='center', fontsize=22)
    plt.subplots_adjust(bottom=0.15, left=0.08, right=0.92)
    
    if output_filename is None:
        suffix = "" if pearson else "_no_pearson"
        if not plot_skew:
            suffix += "_no_skew"
        output_filename = f"pq_openai_line_plot{suffix}"
    elif output_filename.endswith(".pdf"):
        output_filename = output_filename[:-4]
        
    out_path_pdf = OUTPUT_DIR / f"{output_filename}.pdf"
    out_path_png = OUTPUT_DIR / f"{output_filename}.png"
    plt.savefig(out_path_pdf, dpi=300, bbox_inches='tight')
    plt.savefig(out_path_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Line Plot] Generated successfully: {out_path_pdf} and {out_path_png}")
    return out_path_pdf

def generate_recall_comparison_plots(output_filename="pq_openai_recall_delta_with_absolute_recalls"):
    """Generate 2x3 line plot comparing Recall Delta with Uniform & Variable Recalls for PQ + OpenAI."""
    budgets = get_budgets(MODEL_ORIG)
    bpd_array = [b * 8 / MODEL_DIM for b in budgets][1:]
    
    fig = plt.figure(figsize=(22, 7.5))
    inner_gs = gridspec.GridSpec(2, 3, hspace=0.35, wspace=0.35)
    
    grid_layout = []
    row = []
    for ds in DATASETS_GROUP_1.keys():
        data = get_greedy_data(QUANTIZER, ds, MODEL_ORIG)
        uni = get_uniform_recalls(QUANTIZER, ds, MODEL_ORIG)
        var = get_variable_recalls(QUANTIZER, ds, MODEL_ORIG)
        row.append((ds, data, uni, var))
    grid_layout.append(row)
    
    row = []
    for ds in DATASETS_GROUP_2.keys():
        data = get_greedy_data(QUANTIZER, ds, MODEL_ORIG)
        uni = get_uniform_recalls(QUANTIZER, ds, MODEL_ORIG)
        var = get_variable_recalls(QUANTIZER, ds, MODEL_ORIG)
        row.append((ds, data, uni, var))
    grid_layout.append(row)
    
    all_imps = []
    all_group_recalls = []
    for row_data in grid_layout:
        for _, data, uni, var in row_data:
            all_imps.extend(data['imps'][1:])
            all_group_recalls.extend(uni[1:])
            all_group_recalls.extend(var[1:])
            
    imp_ymin = min(all_imps) - 1 if all_imps else 0
    imp_ymax = max(all_imps) + 1 if all_imps else 100
    recall_ymin = min(all_group_recalls) - 5 if all_group_recalls else 0
    recall_ymax = max(all_group_recalls) + 5 if all_group_recalls else 100
    
    for r in range(2):
        for c in range(3):
            ax = fig.add_subplot(inner_gs[r, c])
            dataset_name, data, uni, var = grid_layout[r][c]
            imps = data['imps'][1:]
            uni_sliced = uni[1:]
            var_sliced = var[1:]
            
            l1 = ax.plot(bpd_array, imps, marker='o', color='#1f77b4', linewidth=3, markersize=8, label='Recall $\\Delta$ (%)')
            if c == 0:
                ax.set_ylabel('Recall $\\Delta$ (%)', color='#1f77b4', fontsize=18)
            else:
                ax.set_ylabel('')
            ax.tick_params(axis='y', labelcolor='#1f77b4')
            ax.set_ylim(imp_ymin, imp_ymax)
            
            ax_twin = ax.twinx()
            l2 = ax_twin.plot(bpd_array, uni_sliced, marker='^', color='#999999', linestyle='--', linewidth=2, markersize=6, alpha=0.7, label='Uniform Recall')
            l3 = ax_twin.plot(bpd_array, var_sliced, marker='v', color='#d62728', linestyle='--', linewidth=2, markersize=6, alpha=0.5, label='Variable Recall')
            
            ax_twin.set_ylabel('')
            ax_twin.tick_params(axis='y', labelcolor='#555555')
            ax_twin.set_ylim(recall_ymin, recall_ymax)
            
            ax.set_title(dataset_name.replace('DBPedia', 'DBpedia'), pad=15)
            
            if r == 0 and c == 0:
                row_label = f"{QUANTIZER} / {MODEL_DISPLAY}"
                ax.annotate(row_label, xy=(-0.24, -0.15), xycoords='axes fraction', size=18, ha='right', va='center', rotation=90)
            
            ax.set_xticks(bpd_array)
            if r == 1:
                ax.set_xticklabels([f"{x:.2f}" for x in bpd_array], rotation=90, ha='center', va='top')
            else:
                ax.set_xticklabels([])
                
            if r == 0 and c == 2:
                lns = l1 + l2 + l3
                labs = [l.get_label() for l in lns]
                ax.legend(lns, labs, loc='upper left', framealpha=0.9, edgecolor='black', fontsize=10)
                
            ax.grid(True, linestyle=':', alpha=0.7)
            
    fig.text(0.5, 0.01, 'Bits per Dimension (bpd)', ha='center', va='center', fontsize=22)
    # One common right y-axis label for Absolute Recall@100 (%) (rotation=90)
    fig.text(0.965, 0.52, 'Absolute Recall@100 (%)', ha='center', va='center', rotation=90, fontsize=20, color='#555555')
    plt.subplots_adjust(bottom=0.15, left=0.08, right=0.92)
    
    if output_filename.endswith(".pdf"):
        output_filename = output_filename[:-4]
    out_path_pdf = OUTPUT_DIR / f"{output_filename}.pdf"
    out_path_png = OUTPUT_DIR / f"{output_filename}.png"
    plt.savefig(out_path_pdf, dpi=300, bbox_inches='tight')
    plt.savefig(out_path_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Recall Comparison Plot] Generated successfully: {out_path_pdf} and {out_path_png}")
    return out_path_pdf

# ==============================================================================
# 3. PLOT 2: BIT ALLOCATIONS HEATMAP (PQ + OpenAI)
# ==============================================================================
def generate_heatmap(output_filename="pq_openai_bit_allocations_heatmap"):
    """Generate bit allocations heatmap for PQ and SQ on OpenAI across datasets and budgets (skipping 0.17 bpd)."""
    # Skip 0.17 bpd (first budget 64)
    budgets = get_budgets(MODEL_ORIG)[1:]
    n_budgets = len(budgets)
    quantizers = ['PQ', 'SQ']
    
    alloc_fractions = []
    qm_grid_data = {}
    for quantizer in quantizers:
        qm_grid_data[quantizer] = []
        for ds in DATASET_NAMES:
            data = get_greedy_data(quantizer, ds, MODEL_ORIG)
            qm_grid_data[quantizer].append(data)
            for b_idx_full, b in enumerate(get_budgets(MODEL_ORIG)):
                if b in budgets:
                    alloc_arr = np.array(data['allocs'][b_idx_full], dtype=float)
                    alloc_fractions.extend(alloc_arr / b)
            
    global_min = min(alloc_fractions) if alloc_fractions else 0
    global_max = max(alloc_fractions) if alloc_fractions else 1.0
    
    cmap_hm = cm.YlOrRd
    norm_hm = mcolors.Normalize(vmin=global_min, vmax=global_max)
    
    fig_hm, axes_hm = plt.subplots(len(quantizers), n_budgets, figsize=(28, 10), gridspec_kw={'wspace': 0.06, 'hspace': 0.35})
    
    for q_idx, quantizer in enumerate(quantizers):
        grid_data = qm_grid_data[quantizer]
        for budget_i, b in enumerate(budgets):
            full_b_idx = budget_i + 1
            ax = axes_hm[q_idx, budget_i]
            bpd = b * 8 / MODEL_DIM
            
            matrix = np.array([
                grid_data[ds_i]['allocs'][full_b_idx] for ds_i in range(6)
            ], dtype=float) / b
            
            ax.imshow(matrix, aspect='auto', cmap=cmap_hm, norm=norm_hm, interpolation='nearest')
            
            for y_line in [0.5, 1.5, 3.5, 4.5]:
                ax.axhline(y_line, color='white', linewidth=1.0)
            ax.axhline(2.5, color='white', linewidth=3.0)
            
            if q_idx == 0:
                ax.set_title(f'{bpd:.2f} bpd', fontsize=20)
            
            ax.set_xticks(range(8))
            # Label B1-B8 on only ONE heatmap (bottom-left)
            if q_idx == len(quantizers) - 1 and budget_i == 0:
                ax.set_xticklabels([f'B{i+1}' for i in range(8)], fontsize=18, rotation=90, ha='center', va='top')
            else:
                ax.set_xticklabels([])
            
            if budget_i == 0:
                ax.set_yticks(range(6))
                ax.set_yticklabels([d.replace('DBPedia', 'DBpedia') for d in DATASET_NAMES], fontsize=16)
                ax.set_ylabel(f"{quantizer} / {MODEL_DISPLAY}", fontsize=22, labelpad=8)
            else:
                ax.set_yticks([])
                
    fig_hm.subplots_adjust(right=0.87, left=0.08, bottom=0.10, top=0.92)
    
    # Position colorbar to match exact vertical span of all heatmap rows
    pos_bottom = axes_hm[-1, 0].get_position()
    pos_top = axes_hm[0, 0].get_position()
    cbar_ax = fig_hm.add_axes([0.89, pos_bottom.y0, 0.014, pos_top.y1 - pos_bottom.y0])
    sm = cm.ScalarMappable(cmap=cmap_hm, norm=norm_hm)
    sm.set_array([])
    cbar = fig_hm.colorbar(sm, cax=cbar_ax)
    cbar.set_label('Fraction of total bit budget', fontsize=20, labelpad=18)
    
    if output_filename is None:
        output_filename = "pq_openai_bit_allocations_heatmap"
    elif output_filename.endswith(".pdf"):
        output_filename = output_filename[:-4]
    
    out_path_pdf = OUTPUT_DIR / f"{output_filename}.pdf"
    out_path_png = OUTPUT_DIR / f"{output_filename}.png"
    plt.savefig(out_path_pdf, dpi=300, bbox_inches='tight')
    plt.savefig(out_path_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Heatmap] Generated successfully: {out_path_pdf} and {out_path_png}")
    return out_path_pdf

# ==============================================================================
# 4. PLOT 3: VARIANCE PLOT (OpenAI text-embedding-3-large alone)
# ==============================================================================
def load_full_variance(file_path: Path) -> Tuple[int, np.ndarray]:
    """Read file header and compute dimension-wise variance across ALL vectors using memmap."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    with open(file_path, 'rb') as f:
        npts = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        dim = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        
    print(f"Computing variance across all {npts:,} vectors of dimension {dim} from {file_path.parent.parent.name}/{file_path.parent.name}...")
    
    data = np.memmap(file_path, dtype=np.float32, mode='r', offset=8, shape=(npts, dim))
    
    sum_x = np.zeros(dim, dtype=np.float64)
    sum_x2 = np.zeros(dim, dtype=np.float64)
    
    chunk_size = 50000
    for i in range(0, npts, chunk_size):
        chunk = data[i : min(i + chunk_size, npts)]
        sum_x += np.sum(chunk, axis=0, dtype=np.float64)
        sum_x2 += np.sum(chunk**2, axis=0, dtype=np.float64)
        
    mean = sum_x / npts
    mean_sq = sum_x2 / npts
    variances = mean_sq - mean**2
    
    del data
    return dim, variances

def compute_rolling_mean(arr: np.ndarray, window: int) -> np.ndarray:
    """Compute rolling mean with window size using cumulative sum."""
    cumsum = np.cumsum(np.insert(arr, 0, 0.0))
    out = np.zeros_like(arr)
    for i in range(len(arr)):
        start = max(0, i - window + 1)
        out[i] = (cumsum[i + 1] - cumsum[start]) / (i + 1 - start)
    return out

def generate_variance_plot(window=128, output_filename=None):
    """Generate rolling average variance plot for OpenAI text-embedding-3-large across 6 datasets."""
    datasets = {
        "dbpedia_entity_500k": "DBpedia Entity (500k)",
        "msmarco_500k": "MSMARCO (500k)",
        "quora_500k": "Quora (500k)",
        "fiqa": "FiQA",
        "scidocs": "SciDocs",
        "scifact": "SciFact"
    }
    
    colors = {
        "dbpedia_entity_500k": "#0284c7",  # Tailwind Sky-600
        "msmarco_500k": "#f97316",         # Tailwind Orange-500
        "quora_500k": "#10b981",           # Tailwind Emerald-500
        "fiqa": "#8b5cf6",                 # Tailwind Violet-500
        "scidocs": "#ef4444",              # Tailwind Red-500
        "scifact": "#eab308"               # Tailwind Yellow-500
    }
    
    # Premium styling matching plot_rolling_variance.py
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = '#0f172a'
    plt.rcParams['axes.labelcolor'] = '#334155'
    plt.rcParams['xtick.color'] = '#475569'
    plt.rcParams['ytick.color'] = '#475569'
    
    # Square aspect ratio for OpenAI alone
    fig, ax = plt.subplots(1, 1, figsize=(9, 8), dpi=300)
    dim_limit = MODEL_DIM
    
    skip_dims = 127  # Skip first 127 dimensions, leaving 0-127 area blank
    
    for ds_id, ds_label in datasets.items():
        base_file = EMBEDDINGS_DIR / ds_id / MODEL_KEY / "base.bin"
        try:
            dim, vars_raw = load_full_variance(base_file)
            rolling_vars = compute_rolling_mean(vars_raw, window=window)
            
            ax.plot(np.arange(skip_dims, dim), rolling_vars[skip_dims:], label=ds_label, 
                    color=colors[ds_id], linewidth=2.2, zorder=3)
        except Exception as e:
            print(f"Error processing {ds_id} for {MODEL_KEY}: {e}")
            
    ax.set_xlabel("Dimension Index", fontsize=20, labelpad=8)
    ax.set_ylabel(f"Rolling Mean Variance (Window={window})", fontsize=20, labelpad=10)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xlim(0, dim_limit)  # Starts at 0 to leave 0-127 area blank
    ax.grid(True, which='both', linestyle=':', alpha=0.3, zorder=1)
    ax.legend(fontsize=16, loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
    
    plt.tight_layout()
    
    if output_filename is None:
        output_filename = f"pq_openai_{window}_variance_rolling_average"
    elif output_filename.endswith(".pdf"):
        output_filename = output_filename[:-4]
        
    out_path_pdf = OUTPUT_DIR / f"{output_filename}.pdf"
    out_path_png = OUTPUT_DIR / f"{output_filename}.png"
    plt.savefig(out_path_pdf, dpi=300, bbox_inches='tight')
    plt.savefig(out_path_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Variance Plot] Generated successfully: {out_path_pdf} and {out_path_png}")
    return out_path_pdf

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == '__main__':
    print("=== Generating PQ + OpenAI Plots ===")
    print(f"Results Path:    {RUNS_BASE_DIR}")
    print(f"Embeddings Path: {EMBEDDINGS_DIR}")
    print(f"Output Path:     {OUTPUT_DIR}\n")
    
    # 1. Line plots
    generate_line_plots(pearson=False, plot_skew=False, output_filename="pq_openai_line_plot")
    generate_line_plots(pearson=True, plot_skew=True, output_filename="pq_openai_line_plot_with_skew")
    generate_recall_comparison_plots(output_filename="pq_openai_recall_delta_with_absolute_recalls")
    
    # 2. Heatmap
    generate_heatmap(output_filename="pq_openai_bit_allocations_heatmap")
    
    # 3. Variance plot (using precalculated/memmap)
    generate_variance_plot(window=128, output_filename="pq_openai_128_variance_rolling_average")
    
    print("\n=== All PQ + OpenAI Plots Generated Successfully! ===")
