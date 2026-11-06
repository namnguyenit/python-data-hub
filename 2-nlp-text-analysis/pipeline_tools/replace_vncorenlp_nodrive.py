import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_source = [
    'import pandas as pd\n',
    'import os\n',
    'import py_vncorenlp\n',
    '\n',
    '# Tải model VnCoreNLP về môi trường tạm (Colab/Local) mỗi lần chạy\n',
    '# py_vncorenlp.download_model sẽ tự động bỏ qua nếu đã tải rồi\n',
    'current_dir = "."\n',
    'py_vncorenlp.download_model(save_dir=current_dir)\n',
    '\n',
    '# Khởi tạo VnCoreNLP\n',
    'try:\n',
    '    rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=current_dir)\n',
    '    print("Đã load thành công VnCoreNLP.")\n',
    'except Exception as e:\n',
    '    print(f"Lỗi khởi tạo VnCoreNLP: {e}")\n',
    '    rdrsegmenter = None\n',
    '\n',
    '# 1. Đọc từ điển teencode đã hoàn thiện từ DATA_PATH hoặc thư mục gốc\n',
    'teencode_path = f"{PROJECT_PATH}/teencode.txt"\n',
    'stopwords_path = f"{PROJECT_PATH}/stopwords.txt"\n',
    '\n',
    'teencode_dict = {}\n',
    'if os.path.exists(teencode_path):\n',
    '    with open(teencode_path, \'r\', encoding=\'utf-8\') as f:\n',
    '        for line in f:\n',
    '            parts = line.strip().split(\'\\t\')\n',
    '            if len(parts) == 2:\n',
    '                teencode_dict[parts[0]] = parts[1]\n',
    'else:\n',
    '    print(f"Không tìm thấy file {teencode_path}")\n',
    '\n',
    '# 2. Danh sách stopwords\n',
    'stopwords = set()\n',
    'if os.path.exists(stopwords_path):\n',
    '    with open(stopwords_path, \'r\', encoding=\'utf-8\') as f:\n',
    '        stopwords = set(line.strip() for line in f if line.strip())\n',
    '    print(f"Đã tải {len(stopwords)} stopwords.")\n',
    'else:\n',
    '    print(f"Cảnh báo: Không tìm thấy file {stopwords_path}")\n',
    '\n',
    'def final_clean(text):\n',
    '    if not isinstance(text, str):\n',
    '        return ""\n',
    '    \n',
    '    # 3. Thay thế Teencode\n',
    '    words = text.split()\n',
    '    normalized_words = [teencode_dict.get(w, w) for w in words]\n',
    '    text_after_teencode = \' \'.join(normalized_words)\n',
    '    \n',
    '    # 4. Tokenization (Tách từ bằng VnCoreNLP)\n',
    '    if rdrsegmenter:\n',
    '        try:\n',
    '            sentences = rdrsegmenter.word_segment(text_after_teencode)\n',
    '            tokenized_text = \' \'.join(sentences)\n',
    '        except Exception:\n',
    '            tokenized_text = text_after_teencode\n',
    '    else:\n',
    '        tokenized_text = text_after_teencode\n',
    '    \n',
    '    # 5. Loại bỏ Stopwords\n',
    '    final_words = [w for w in tokenized_text.split() if w not in stopwords]\n',
    '    \n',
    '    return \' \'.join(final_words)\n',
    '\n',
    'print("Đang áp dụng làm sạch bước cuối và tách từ...")\n',
    '\n',
    '# Đọc lại file kết quả từ bước 1\n',
    'step1_data_path = f"{DATA_PATH}/cleaned_step1_dataset.csv"\n',
    'df_final = pd.read_csv(step1_data_path, encoding=\'utf-8\')\n',
    '\n',
    '# Áp dụng hàm final_clean\n',
    'df_final[\'text\'] = df_final[\'text\'].apply(final_clean)\n',
    '\n',
    '# Lưu ra file csv cuối cùng\n',
    'final_output_path = f"{DATA_PATH}/final_cleaned_dataset.csv"\n',
    'df_final[[\'text\', \'label\']].to_csv(final_output_path, index=False, encoding=\'utf-8\')\n',
    '\n',
    'print(f"\\nHOÀN THÀNH TOÀN BỘ CÂU A3! Đã lưu tại: {final_output_path}")\n',
    'display(df_final.head(10))\n'
]

for cell in reversed(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if 'def final_clean(text):' in source:
            cell['source'] = new_source
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Updated notebook to download model to current dir and run directly.")
