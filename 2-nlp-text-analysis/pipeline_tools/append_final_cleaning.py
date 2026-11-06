import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells_to_add = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Bước 2: Chuẩn hóa Teencode, Tách từ (Tokenization) và Loại bỏ Stopwords\n',
            'Đây là bước cuối cùng trong pipeline tiền xử lý (Câu A3), giúp chúng ta tạo ra tập dữ liệu `final_cleaned_dataset.csv` sẵn sàng để huấn luyện mô hình.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            '# Cài đặt thư viện tách từ tiếng Việt underthesea (nếu chưa có chạy dòng dưới)\n',
            '# !pip install underthesea'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import pandas as pd\n',
            '# from underthesea import word_tokenize # Mở comment dòng này nếu bạn muốn dùng underthesea tách từ thành "sản_phẩm"\n',
            '\n',
            '# 1. Đọc từ điển teencode đã hoàn thiện\n',
            'teencode_dict = {}\n',
            'with open(\'teencode.txt\', \'r\', encoding=\'utf-8\') as f:\n',
            '    for line in f:\n',
            '        parts = line.strip().split(\'\\t\')\n',
            '        if len(parts) == 2:\n',
            '            teencode_dict[parts[0]] = parts[1]\n',
            '\n',
            '# 2. Danh sách stopwords (Từ dừng)\n',
            '# LƯU Ý QUAN TRỌNG: Với bài toán Sentiment Analysis (Phân tích cảm xúc),\n',
            '# TUYỆT ĐỐI KHÔNG xóa các từ mang ý nghĩa phủ định/khẳng định (không, chẳng, rất, quá...).\n',
            '# Chỉ xóa các từ nối, đại từ, giới từ không mang sắc thái cảm xúc.\n',
            'stopwords = set(["là", "thì", "mà", "của", "các", "những", "ở", "tại", "này", "kia", "đó", "đây", "và", "với", "như", "một", "sự", "những", "cái"])\n',
            '\n',
            'def final_clean(text):\n',
            '    if not isinstance(text, str):\n',
            '        return ""\n',
            '        \n',
            '    # 3. Thay thế Teencode & Sửa lỗi không dấu\n',
            '    words = text.split()\n',
            '    normalized_words = [teencode_dict.get(w, w) for w in words]\n',
            '    text_after_teencode = \' \'.join(normalized_words)\n',
            '    \n',
            '    # 4. Tokenization (Tách từ)\n',
            '    # Nếu bạn dùng underthesea thì bật dòng dưới đây, nếu không thì để mặc định split bằng khoảng trắng.\n',
            '    # tokenized_text = word_tokenize(text_after_teencode, format="text")\n',
            '    tokenized_text = text_after_teencode\n',
            '    \n',
            '    # 5. Loại bỏ Stopwords\n',
            '    final_words = [w for w in tokenized_text.split() if w not in stopwords]\n',
            '    \n',
            '    # 6. Lemmatization/Stemming: Tiếng Việt không biến đổi hình thái từ (ngôi, số, thời, thể)\n',
            '    # nên bản chất bước chuẩn hóa chữ thường và teencode ở trên đã đóng vai trò tương tự Lemmatization.\n',
            '    \n',
            '    return \' \'.join(final_words)\n',
            '\n',
            'print("Đang áp dụng từ điển teencode và làm sạch bước cuối...")\n',
            '\n',
            '# Đọc lại file của bước 1\n',
            'step1_data_path = f"{DATA_PATH}/cleaned_step1_dataset.csv"\n',
            'df_final = pd.read_csv(step1_data_path, encoding=\'utf-8\')\n',
            '\n',
            '# Áp dụng pipeline\n',
            'df_final[\'text\'] = df_final[\'text\'].apply(final_clean)\n',
            '\n',
            '# Lưu ra file csv cuối cùng\n',
            'final_output_path = f"{DATA_PATH}/final_cleaned_dataset.csv"\n',
            'df_final[[\'text\', \'label\']].to_csv(final_output_path, index=False, encoding=\'utf-8\')\n',
            '\n',
            'print(f"\\nHOÀN THÀNH TOÀN BỘ CÂU A3! Đã lưu tập dữ liệu cuối cùng tại: {final_output_path}")\n',
            'display(df_final.head(10))'
        ]
    }
]

nb['cells'].extend(cells_to_add)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Appended final cleaning cells.")
