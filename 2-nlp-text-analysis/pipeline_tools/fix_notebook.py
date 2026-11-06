import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the index of Cell 26 (which is "**Câu A3**")
# I'll just look for the cell containing "**Câu A3**" to be safe.
cutoff_idx = len(nb['cells'])
for i, cell in enumerate(nb['cells']):
    source = cell.get('source', [])
    if isinstance(source, list) and any('**Câu A3**' in line for line in source):
        cutoff_idx = i + 1
        break

# Keep only cells up to cutoff_idx
nb['cells'] = nb['cells'][:cutoff_idx]

# Append the correct cells
correct_cells = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Bước 1: Chuyển về chữ thường, loại bỏ URL, ký tự đặc biệt'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import re\n',
            '\n',
            'def clean_basic(text):\n',
            '    if not isinstance(text, str):\n',
            '        return ""\n',
            '        \n',
            '    # 1. Chuyển về chữ thường\n',
            '    text = text.lower()\n',
            '    \n',
            '    # 2. Loại bỏ URLs\n',
            '    text = re.sub(r\'http\\S+|www\\.\\S+\', \' \', text)\n',
            '    \n',
            '    # 3. Loại bỏ ký tự đặc biệt (giữ lại chữ, số và tiếng Việt)\n',
            '    vietnamese_chars = \'a-zA-Z0-9\\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\'\n',
            '    pattern = r\'[^\' + vietnamese_chars + \']\'\n',
            '    text = re.sub(pattern, \' \', text)\n',
            '    \n',
            '    # 4. Xóa khoảng trắng thừa\n',
            '    text = \' \'.join(text.split())\n',
            '    \n',
            '    return text\n',
            '\n',
            'print("Đang xử lý làm sạch dữ liệu...")\n',
            '# Chú ý: Dùng dataframe `data` theo đúng thiết lập ở đầu file\n',
            'data[\'cleaned_text\'] = data[\'text\'].apply(clean_basic)\n',
            '\n',
            '# Lưu ra file CSV mới dùng biến DATA_PATH\n',
            'output_path = f"{DATA_PATH}/cleaned_step1_dataset.csv"\n',
            'data.to_csv(output_path, index=False, encoding=\'utf-8\')\n',
            '\n',
            'print(f"Đã lưu tập dữ liệu sau khi làm sạch bước 1 vào: {output_path}")\n',
            '\n',
            '# Hiển thị thử vài dòng để so sánh\n',
            'data[[\'text\', \'cleaned_text\', \'label\']].head()'
        ]
    }
]

nb['cells'].extend(correct_cells)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook has been fixed.")
