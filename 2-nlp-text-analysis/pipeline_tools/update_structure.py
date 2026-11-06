import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in reversed(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        # Find the cell we just added
        if any('def clean_basic(text):' in line for line in source):
            new_source = []
            for line in source:
                if 'data[\'cleaned_text\'] = data[\'text\'].apply(clean_basic)' in line:
                    new_source.append('data[\'text\'] = data[\'text\'].apply(clean_basic)\n')
                elif 'data[[\'text\', \'cleaned_text\', \'label\']].head()' in line:
                    new_source.append('data.head()\n')
                else:
                    new_source.append(line)
            cell['source'] = new_source
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Updated notebook to keep original structure.")
