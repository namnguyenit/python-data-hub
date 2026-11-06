import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    source = cell.get('source', [])
    if not source: continue
    
    # Update pip install cell
    if any('!pip install underthesea' in line for line in source):
        cell['source'] = [
            '# Cài đặt thư viện VnCoreNLP (nếu chưa có chạy dòng dưới)\n',
            '# !pip install py_vncorenlp'
        ]
        continue

    # Update the final_clean cell
    if any('def final_clean(text):' in line for line in source):
        new_source = []
        skip_import = False
        skip_tokenize = False
        for line in source:
            if 'import pandas as pd' in line:
                new_source.extend([
                    'import pandas as pd\n',
                    'import py_vncorenlp\n',
                    'import os\n',
                    '\n',
                    '# Tải model VnCoreNLP nếu chưa có (Tháo comment dòng dưới nếu chạy lần đầu trên Colab)\n',
                    'vncorenlp_dir = f"{PROJECT_PATH}/VnCoreNLP"\n',
                    '# py_vncorenlp.download_model(save_dir=vncorenlp_dir)\n',
                    '\n',
                    'try:\n',
                    '    rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=vncorenlp_dir)\n',
                    '    print("Đã load thành công VnCoreNLP.")\n',
                    'except Exception as e:\n',
                    '    print(f"Chưa tìm thấy model VnCoreNLP. Vui lòng tải model trước: {e}")\n',
                    '    rdrsegmenter = None\n',
                    '\n'
                ])
                skip_import = True
            elif '# from underthesea import word_tokenize' in line and skip_import:
                pass # skip old line
            
            # Replace tokenization logic
            elif '# 4. Tokenization (Tách từ)' in line:
                new_source.append('    # 4. Tokenization bằng VnCoreNLP\n')
                new_source.append('    if rdrsegmenter:\n')
                new_source.append('        try:\n')
                new_source.append('            sentences = rdrsegmenter.word_segment(text_after_teencode)\n')
                new_source.append('            tokenized_text = " ".join(sentences)\n')
                new_source.append('        except Exception:\n')
                new_source.append('            tokenized_text = text_after_teencode\n')
                new_source.append('    else:\n')
                new_source.append('        tokenized_text = text_after_teencode\n')
                skip_tokenize = True
            elif skip_tokenize and ('tokenized_text =' in line or 'Nếu bạn dùng underthesea' in line):
                pass # skipping old lines
            elif skip_tokenize and '# 5. Loại bỏ Stopwords' in line:
                skip_tokenize = False
                new_source.append(line)
            else:
                if not skip_tokenize and not ('# from underthesea import word_tokenize' in line):
                    new_source.append(line)
                    
        cell['source'] = new_source

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Updated notebook to use VnCoreNLP.")
