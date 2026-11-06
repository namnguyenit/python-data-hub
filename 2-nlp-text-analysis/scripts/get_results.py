import json

path = 'd:\\PROJECT\\phantichdulieu\\Phân_tích_python.ipynb'
try:
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'code' and 'outputs' in cell:
            for out in cell['outputs']:
                if out.get('output_type') == 'stream':
                    text = "".join(out.get('text', []))
                    if 'accuracy' in text.lower() or 'precision' in text.lower() or 'f1' in text.lower() or 'svm' in text.lower() or 'naive' in text.lower() or 'logistic' in text.lower() or 'random' in text.lower() or 'best' in text.lower() or 'cv' in text.lower():
                        print(f"--- Cell {i} Output ---")
                        print(text)
                if out.get('output_type') in ['execute_result', 'display_data']:
                    data = out.get('data', {})
                    if 'text/plain' in data:
                        text = "".join(data['text/plain'])
                        if 'accuracy' in text.lower() or 'precision' in text.lower() or 'f1' in text.lower() or 'svm' in text.lower() or 'naive' in text.lower() or 'logistic' in text.lower() or 'random' in text.lower() or 'best' in text.lower() or 'cv' in text.lower():
                            print(f"--- Cell {i} Output ---")
                            print(text)
except Exception as e:
    print(f"Error: {e}")
