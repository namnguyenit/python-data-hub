import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in reversed(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        if any('def clean_basic(text):' in line for line in source):
            new_source = []
            for line in source:
                if 'data.to_csv(output_path, index=False, encoding=\'utf-8\')' in line:
                    # Save only text and label columns
                    new_source.append('data[[\'text\', \'label\']].to_csv(output_path, index=False, encoding=\'utf-8\')\n')
                elif 'data.head()' in line:
                    # Display only text and label columns
                    new_source.append('data[[\'text\', \'label\']].head()\n')
                else:
                    new_source.append(line)
            cell['source'] = new_source
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Updated notebook to only save and display text and label columns.")
