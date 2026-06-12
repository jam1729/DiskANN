import re
from pathlib import Path

# Mapping tables
DATASETS_MAP = {
    'MS Marco': 'msmarco_500k',
    'DBPedia': 'dbpedia_entity_500k',
    'Quora': 'quora_500k'
}

MODELS_MAP = {
    'OAI text-embed-3-l': 'openai_text_large_3',
    'Cohere embed-v4': 'cohere_v4'
}

BASE_DIR = Path('/home/jam1729/runs/workshop_results')

def parse_uniform(file_path):
    budgets = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
    lines = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            lines.append(line)
            
    assert len(lines) == 11, f"Expected 11 non-empty lines in {file_path}, got {len(lines)}"
    
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

def parse_variable(file_path):
    init_entry = None
    it_lines = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if 'tag=init' in line and 'bytes=64' in line:
                alloc_match = re.search(r'alloc=\[(.*?)\]', line)
                bytes_match = re.search(r'bytes=(\d+)', line)
                recall_match = re.search(r'recall=([\d.]+)', line)
                if alloc_match and bytes_match and recall_match:
                    alloc = [int(x.strip()) for x in alloc_match.group(1).split(',')]
                    b = int(bytes_match.group(1))
                    recall = float(recall_match.group(1))
                    init_entry = {'alloc': alloc, 'bytes': b, 'recall': recall}
            elif 'tag=it' in line:
                it_lines.append(line)
                
    assert len(it_lines) == 320, f"Expected 320 iteration lines, got {len(it_lines)} in {file_path}"
    assert init_entry is not None, f"Expected tag=init with bytes=64 in {file_path}"
    
    parsed_entries = [init_entry]
    for line in it_lines:
        alloc_match = re.search(r'alloc=\[(.*?)\]', line)
        bytes_match = re.search(r'bytes=(\d+)', line)
        recall_match = re.search(r'recall=([\d.]+)', line)
        
        assert alloc_match and bytes_match and recall_match, f"Failed to parse line: {line}"
        
        alloc = [int(x.strip()) for x in alloc_match.group(1).split(',')]
        b = int(bytes_match.group(1))
        recall = float(recall_match.group(1))
        
        parsed_entries.append({'alloc': alloc, 'bytes': b, 'recall': recall})
        
    by_bytes = {}
    for entry in parsed_entries:
        b = entry['bytes']
        if b not in by_bytes:
            by_bytes[b] = []
        by_bytes[b].append(entry)
        
    best_by_bytes = {}
    for b, entries in by_bytes.items():
        best_entry = max(entries, key=lambda x: (x['recall'], x['alloc']))
        best_by_bytes[b] = (best_entry['alloc'], best_entry['recall'])
        
    return best_by_bytes

def get_greedy_data(quantizer, dataset, model):
    dir_path = BASE_DIR / quantizer.lower() / DATASETS_MAP[dataset] / MODELS_MAP[model]
    uni_data = parse_uniform(dir_path / 'uniform.txt')
    var_data = parse_variable(dir_path / 'variable.txt')
    
    budgets = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
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
    dir_path = BASE_DIR / quantizer.lower() / DATASETS_MAP[dataset] / MODELS_MAP[model]
    uni_data = parse_uniform(dir_path / 'uniform.txt')
    budgets = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
    return [uni_data[b] for b in budgets]

def get_variable_recalls(quantizer, dataset, model):
    dir_path = BASE_DIR / quantizer.lower() / DATASETS_MAP[dataset] / MODELS_MAP[model]
    var_data = parse_variable(dir_path / 'variable.txt')
    budgets = [64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
    return [var_data[b][1] for b in budgets]

if __name__ == '__main__':
    for q in ['pq', 'sq']:
        print(f"\n==================== {q.upper()} ====================")
        for ds in DATASETS_MAP.keys():
            for m in MODELS_MAP.keys():
                data = get_greedy_data(q, ds, m)
                print(f"{ds} | {m}:")
                print(f"  Allocs: {data['allocs']}")
                print(f"  Imps:   {[round(x, 2) for x in data['imps']]}")
