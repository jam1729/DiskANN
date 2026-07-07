import json
with open('figures_updated.py', 'r') as f:
    content = f.read()

cells_text = content.split('# CELL ')[1:]

with open('figures_updated.ipynb', 'r') as f:
    data = json.load(f)

code_cell_idx = 0
for cell in data.get('cells', []):
    if cell['cell_type'] == 'code':
        if code_cell_idx < len(cells_text):
            cell_text = cells_text[code_cell_idx]
            lines = cell_text.split('\n', 1)[1].splitlines(keepends=True)
            cell['source'] = lines
            cell['outputs'] = []
            cell['execution_count'] = None
        code_cell_idx += 1

with open('figures_updated.ipynb', 'w') as f:
    json.dump(data, f, indent=1)
