import json

with open('d:\\PROJECT\\phantichdulieu\\Phân_tích_python.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell['cell_type'] == 'code':
        source = "".join(cell.get('source', []))
        for out in cell.get('outputs', []):
            text = ""
            if out.get('output_type') == 'stream':
                text = "".join(out.get('text', []))
            elif out.get('output_type') in ['display_data', 'execute_result']:
                if 'text/plain' in out.get('data', {}):
                    text = "".join(out.get('data', {})['text/plain'])
            if 'macro avg' in text or 'accuracy' in text.lower():
                if 'Naive' in source or 'MultinomialNB' in source:
                    print("--- Naive Bayes Output ---")
                    print(text)
