import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find where to replace or append
# We will just remove the previous "Khám phá và Phát hiện" cells if they exist, and add the new one.
new_cells = []
skip = False
for cell in nb['cells']:
    source = cell.get('source', [])
    if isinstance(source, list) and any('Khám phá và Phát hiện Teen Code' in line for line in source):
        skip = True
    if not skip:
        new_cells.append(cell)

nb['cells'] = new_cells

cells_to_add = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Bước phụ trợ: Trích xuất Teencode để định nghĩa thủ công\n',
            'Đoạn code dưới đây sẽ quét dữ liệu, tìm ra các từ không có dấu (khả năng cao là tiếng lóng/teencode) và xuất ra một file text `unlabeled_teencodes.txt`. Nhiệm vụ của bạn là mở file này lên và tự định nghĩa nghĩa tiếng Việt chuẩn cho từng từ.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import pandas as pd\n',
            'from collections import Counter\n',
            '\n',
            'print("Đang quét dữ liệu để tìm teen code...")\n',
            '# 1. Đọc dữ liệu vừa được làm sạch ở bước 1\n',
            'step1_data_path = f"{DATA_PATH}/cleaned_step1_dataset.csv"\n',
            'df_step1 = pd.read_csv(step1_data_path, encoding=\'utf-8\')\n',
            '\n',
            '# 2. Đếm tần suất từ\n',
            'word_counter = Counter()\n',
            'for text in df_step1[\'text\'].dropna():\n',
            '    word_counter.update(text.split())\n',
            '\n',
            '# 3. Lọc từ tiềm năng (các từ không có dấu tiếng Việt)\n',
            'vietnamese_vowels_accents = \'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\'\n',
            'potential_teencodes = []\n',
            '\n',
            '# Lấy top 500 từ xuất hiện nhiều nhất (bạn có thể tăng số này lên)\n',
            'for word, count in word_counter.most_common(500):\n',
            '    if len(word) < 2 and word not in ["k", "m", "t", "j", "v", "z", "q"]:\n',
            '        continue\n',
            '    \n',
            '    has_accent = any(char in vietnamese_vowels_accents for char in word)\n',
            '    if not has_accent:\n',
            '        potential_teencodes.append(word)\n',
            '\n',
            '# 4. Xuất ra file txt để định nghĩa thủ công\n',
            'output_txt = f"{DATA_PATH}/unlabeled_teencodes.txt"\n',
            'with open(output_txt, \'w\', encoding=\'utf-8\') as f:\n',
            '    for word in potential_teencodes:\n',
            '        # Ghi từ ra file kèm dấu Tab (\\t) để sẵn khoảng trống cho bạn điền nghĩa\n',
            '        f.write(f"{word}\\t\\n")\n',
            '\n',
            'print(f"\\nThành công! Đã trích xuất {len(potential_teencodes)} từ tiềm năng ra file: {output_txt}")\n',
            'print("=> Vui lòng mở file này, điền nghĩa chuẩn vào sau mỗi dấu tab, và đổi tên/lưu lại thành teencode.txt")'
        ]
    }
]

nb['cells'].extend(cells_to_add)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Appended teencode export logic.")
