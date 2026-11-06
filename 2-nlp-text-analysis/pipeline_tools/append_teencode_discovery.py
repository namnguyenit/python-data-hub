import json
import os

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells_to_add = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Bước phụ trợ: Khám phá và Phát hiện Teen Code tiềm năng\n',
            'Trước khi tiến hành chuẩn hóa Teen Code và Tokenization, chúng ta cần tìm xem trong tập dữ liệu thực tế này có những từ lóng/teencode nào xuất hiện nhiều nhưng chưa có mặt trong từ điển `teencode.txt`.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import pandas as pd\n',
            'import re\n',
            'from collections import Counter\n',
            '\n',
            '# 1. Đọc dữ liệu vừa được làm sạch ở bước 1\n',
            'step1_data_path = f"{DATA_PATH}/cleaned_step1_dataset.csv"\n',
            'df_step1 = pd.read_csv(step1_data_path, encoding=\'utf-8\')\n',
            '\n',
            '# 2. Đọc từ điển teencode hiện tại để loại trừ\n',
            'existing_teencode = set()\n',
            'try:\n',
            '    with open(\'teencode.txt\', \'r\', encoding=\'utf-8\') as f:\n',
            '        for line in f:\n',
            '            parts = line.strip().split(\'\\t\')\n',
            '            if len(parts) > 0:\n',
            '                existing_teencode.add(parts[0])\n',
            '    print(f"Đã tải {len(existing_teencode)} từ teencode hiện có.")\n',
            'except FileNotFoundError:\n',
            '    print("Không tìm thấy file teencode.txt ở thư mục hiện tại. Nếu bạn dùng Colab, hãy tải nó lên.")\n',
            '\n',
            '# 3. Đếm tần suất từ\n',
            'word_counter = Counter()\n',
            '\n',
            'for text in df_step1[\'text\'].dropna():\n',
            '    # Văn bản đã làm sạch, chỉ cần split bằng khoảng trắng\n',
            '    words = text.split()\n',
            '    word_counter.update(words)\n',
            '\n',
            '# 4. Lọc từ tiềm năng\n',
            '# Các ký tự nguyên âm tiếng Việt (có dấu)\n',
            'vietnamese_vowels_accents = \'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\'\n',
            'potential_teencodes = []\n',
            '\n',
            'for word, count in word_counter.most_common():\n',
            '    # Bỏ qua từ quá ngắn (1 ký tự thường không mang nhiều ý nghĩa ngoại trừ k, m, t, j)\n',
            '    if len(word) < 2 and word not in ["k", "m", "t", "j", "v", "z"]:\n',
            '        continue\n',
            '        \n',
            '    # Nếu đã có trong từ điển thì bỏ qua\n',
            '    if word in existing_teencode:\n',
            '        continue\n',
            '        \n',
            '    # Kiểm tra xem từ có chứa nguyên âm có dấu không. \n',
            '    # Teencode thường viết tắt và không gõ dấu (vd: chx, dc, sp, cx, ...)\n',
            '    has_accent = any(char in vietnamese_vowels_accents for char in word)\n',
            '    \n',
            '    if not has_accent:\n',
            '        potential_teencodes.append((word, count))\n',
            '\n',
            '# Hiển thị top 60 từ đáng ngờ nhất\n',
            'print("Top 60 từ có khả năng là teencode chưa được cập nhật:")\n',
            'potential_df = pd.DataFrame(potential_teencodes[:60], columns=[\'Từ\', \'Tần suất\'])\n',
            'display(potential_df)'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '**HÀNH ĐỘNG CỦA BẠN:**\n',
            'Hãy quan sát bảng kết quả trên. Với những từ mà bạn cho là teencode thực sự (ví dụ: `đc`, `k`, `ko`, `sp`, `auth`, `nhìu`, `lun`...), hãy **Mở file `teencode.txt`** và thêm chúng vào cuối file theo định dạng:\n',
            '`<từ lóng>[Tab]<từ chuẩn>`\n',
            '\n',
            '*Ví dụ:*\n',
            '```\n',
            'lun\tluôn\n',
            'nhìu\tnhiều\n',
            'chx\tchưa\n',
            'dc\tđược\n',
            '```\n',
            'Sau khi cập nhật xong, hãy lưu file `teencode.txt` lại.'
        ]
    }
]

nb['cells'].extend(cells_to_add)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Successfully appended Teencode Discovery cells to notebook.')
