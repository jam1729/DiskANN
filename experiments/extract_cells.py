import json

with open('/home/jam1729/DiskANN/experiments/figures_updated.ipynb', 'r') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        print(f"### CELL {i} ###")
        print("".join(cell['source']))
        print("\n")
