with open('figures_updated.py', 'r') as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if line.startswith('def generate_recall_comparison_plots()'):
        start_idx = i
        break

if start_idx != -1:
    lines = lines[:start_idx]
    with open('figures_updated.py', 'w') as f:
        f.writelines(lines)
        with open('rewrite_cell.py', 'r') as r:
            f.write(r.read())
