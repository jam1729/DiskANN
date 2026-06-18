import re
from pathlib import Path

# Mapping tables
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

MODELS_MAP = {
    'OAI text-embed-3-l': 'openai_text_large_3',
    'Cohere embed-v4': 'cohere_v4'
}

BASE_DIR = Path('/home/jam1729/runs/results')

def get_budgets(model):
    if model == 'Cohere embed-v4':
        return [48, 64, 80, 96, 112, 128, 144, 160, 176, 192]
    else:
        return [96, 128, 160, 192, 224, 256, 288, 320, 352, 384]

def get_expected_uniform_lines(model):
    if model == 'Cohere embed-v4':
        return 11 # 32, 48, 64, ..., 192
    else:
        return 11 # 64, 96, ..., 384

def parse_uniform(file_path, model):
    budgets = get_budgets(model)
    expected_lines = get_expected_uniform_lines(model)
    
    lines = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
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

def parse_variable(file_path, model):
    lines_parsed = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            lines_parsed.append(line)
                
    # Initial line + 40 iterations * 8 steps = 321 lines usually. But user said "Ensure it has 40 iterations and 8 steps per iteration (320 non empty lines)."
    # Let's just find all lines that match alloc, bytes, recall.
    
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
            
    # Depending on how the file is written, it might have exactly 320 non-empty lines, or 321.
    # The user rule: "Ensure it has 40 iterations and 8 steps per iteration (320 non empty lines)."
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

def get_greedy_data(quantizer, dataset, model):
    dir_path = BASE_DIR / quantizer.lower() / ALL_DATASETS[dataset] / MODELS_MAP[model]
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

def get_uniform_recalls(quantizer, dataset, model):
    dir_path = BASE_DIR / quantizer.lower() / ALL_DATASETS[dataset] / MODELS_MAP[model]
    uni_data = parse_uniform(dir_path / 'uniform.txt', model)
    budgets = get_budgets(model)
    return [uni_data[b] for b in budgets]

def get_variable_recalls(quantizer, dataset, model):
    dir_path = BASE_DIR / quantizer.lower() / ALL_DATASETS[dataset] / MODELS_MAP[model]
    var_data = parse_variable(dir_path / 'variable.txt', model)
    budgets = get_budgets(model)
    return [var_data[b][1] for b in budgets]

if __name__ == '__main__':
    for q in ['pq', 'sq']:
        print(f"\n==================== {q.upper()} ====================")
        for ds in ALL_DATASETS.keys():
            for m in MODELS_MAP.keys():
                data = get_greedy_data(q, ds, m)
                print(f"{ds} | {m}:")
                print(f"  Allocs: {data['allocs']}")
                print(f"  Imps:   {[round(x, 2) for x in data['imps']]}")
