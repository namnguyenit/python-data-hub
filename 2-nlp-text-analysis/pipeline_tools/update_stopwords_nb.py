import json
import os

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in reversed(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        # Find the cell we just added
        if any('def final_clean(text):' in line for line in source):
            new_source = []
            skip = False
            for line in source:
                if 'stopwords = set(["là"' in line:
                    new_source.extend([
                        '# Đọc danh sách stopwords từ file\n',
                        'stopwords = set()\n',
                        'with open(\'stopwords.txt\', \'r\', encoding=\'utf-8\') as f:\n',
                        '    stopwords = set(line.strip() for line in f if line.strip())\n',
                        'print(f"Đã tải {len(stopwords)} stopwords.")\n'
                    ])
                else:
                    new_source.append(line)
            cell['source'] = new_source
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Updated notebook to read stopwords from file.")
