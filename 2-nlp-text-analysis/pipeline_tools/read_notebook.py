import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for i, cell in enumerate(nb.get('cells', [])):
        print(f"\n--- Cell {i} ({cell.get('cell_type')}) ---")
        source = cell.get('source', [])
        if isinstance(source, list):
            print("".join(source))
        else:
            print(source)
except Exception as e:
    print(f"Error reading notebook: {e}")
