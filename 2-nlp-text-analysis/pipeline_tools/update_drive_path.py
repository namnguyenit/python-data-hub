import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in reversed(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        # Check if this is the apply and save cell
        if any('output_path = \'data/cleaned_step1_dataset.csv\'' in line for line in source):
            new_source = []
            for line in source:
                if 'output_path = \'data/cleaned_step1_dataset.csv\'' in line:
                    new_source.extend([
                        '# TRÊN GOOGLE COLAB:\n',
                        '# Xóa dấu # ở 3 dòng dưới đây nếu bạn đang chạy trên Google Colab để lưu thẳng vào Google Drive\n',
                        '# from google.colab import drive\n',
                        '# drive.mount(\'/content/drive\')\n',
                        '# output_path = \'/content/drive/MyDrive/data/cleaned_step1_dataset.csv\'\n',
                        '\n',
                        '# MẶC ĐỊNH LƯU TRÊN MÁY LOKAL (Hoặc thư mục cùng cấp)\n',
                        'output_path = \'data/cleaned_step1_dataset.csv\'\n'
                    ])
                else:
                    new_source.append(line)
            cell['source'] = new_source
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Updated notebook to include Google Drive Colab paths.')
