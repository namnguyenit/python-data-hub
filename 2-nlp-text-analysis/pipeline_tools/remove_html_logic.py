import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        # Check if this is the clean_basic cell
        if any('def clean_basic(text):' in line for line in source):
            new_source = []
            for line in source:
                if '# 2. Loại bỏ HTML tags' in line:
                    continue
                if 're.sub(r\'<.*?>\', \' \', text)' in line:
                    continue
                new_source.append(line)
            cell['source'] = new_source

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Removed HTML tag stripping logic from notebook.')
