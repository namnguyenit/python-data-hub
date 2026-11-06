import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells_to_add = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '## A.2 Tiền xử lý văn bản\n',
            '### Câu A3 — Làm sạch văn bản\n',
            'Bước 1: Chuyển về chữ thường, loại bỏ HTML tags, URL, và ký tự đặc biệt.'
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
            '        return \"\"\n',
            '        \n',
            '    # 1. Chuyển về chữ thường\n',
            '    text = text.lower()\n',
            '    \n',
            '    # 2. Loại bỏ HTML tags\n',
            '    text = re.sub(r\'<.*?>\', \' \', text)\n',
            '    \n',
            '    # 3. Loại bỏ URLs\n',
            '    text = re.sub(r\'http\\S+|www\\.\\S+\', \' \', text)\n',
            '    \n',
            '    # 4. Loại bỏ ký tự đặc biệt (chỉ giữ lại chữ cái, số, khoảng trắng và ký tự tiếng Việt)\n',
            '    # Lưu ý: Các ký tự tiếng Việt có dấu cũng phải được giữ lại\n',
            '    vietnamese_chars = \'a-zA-Z0-9\\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\'\n',
            '    pattern = r\'[^\' + vietnamese_chars + \']\'\n',
            '    text = re.sub(pattern, \' \', text)\n',
            '    \n',
            '    # 5. Xóa khoảng trắng thừa\n',
            '    text = \' \'.join(text.split())\n',
            '    \n',
            '    return text\n',
            '\n',
            '# Test thử hàm vừa viết\n',
            'sample_text = \"Hàng quá đẹppppp <3 <3 <br> Link mua: https://shopee.vn/abc, Mọi người tham khảo nha!!! 10đ\"\n',
            'print(\"Gốc:\", sample_text)\n',
            'print(\"Sạch:\", clean_basic(sample_text))'
        ]
    }
]

nb['cells'].extend(cells_to_add)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Successfully appended Step 1 of A3 cells to notebook.')
