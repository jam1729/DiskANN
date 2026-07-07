import json

with open('/home/jam1729/DiskANN/experiments/figures_updated.ipynb', 'r') as f:
    nb = json.load(f)

code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']

with open('/home/jam1729/DiskANN/experiments/figures_updated.py', 'w') as f:
    for i, cell in enumerate(code_cells):
        f.write(f"# CELL {i}\n")
        f.write("".join(cell['source']))
        if i < len(code_cells) - 1:
            f.write("\n\n")
