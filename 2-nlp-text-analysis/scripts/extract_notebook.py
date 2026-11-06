import json

try:
    with open('d:\\PROJECT\\phantichdulieu\\Phân_tích_python.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)

    output = []
    for i, cell in enumerate(nb.get('cells', [])):
        cell_type = cell['cell_type']
        source = ''.join(cell['source'])
        output.append(f"--- Cell {i} ({cell_type}) ---")
        output.append(source)
        output.append("")

    with open('d:\\PROJECT\\phantichdulieu\\notebook_clean.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    print("Successfully extracted notebook.")
except Exception as e:
    print(f"Error: {e}")
