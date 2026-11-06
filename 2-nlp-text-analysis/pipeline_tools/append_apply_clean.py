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
            '**Áp dụng hàm làm sạch vào dataset và lưu trữ:**\n',
            'Bây giờ chúng ta sẽ áp dụng hàm `clean_basic` lên toàn bộ cột `text` của tập dữ liệu `final_balanced_dataset.csv`, sau đó lưu kết quả ra một file mới trong thư mục `data/`.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import os\n',
            '\n',
            '# Kiểm tra và load lại df nếu cần\n',
            'if \'df\' not in locals():\n',
            '    df = pd.read_csv(\'final_balanced_dataset.csv\')\n',
            '\n',
            '# Tạo thư mục data nếu chưa có\n',
            'os.makedirs(\'data\', exist_ok=True)\n',
            '\n',
            'print(\"Đang xử lý làm sạch dữ liệu (có thể mất vài giây)...\")\n',
            '# Áp dụng hàm làm sạch\n',
            'df[\'cleaned_text\'] = df[\'text\'].apply(clean_basic)\n',
            '\n',
            '# Lưu ra file CSV mới\n',
            'output_path = \'data/cleaned_step1_dataset.csv\'\n',
            'df.to_csv(output_path, index=False, encoding=\'utf-8\')\n',
            '\n',
            'print(f\"Đã lưu tập dữ liệu sau khi làm sạch bước 1 vào: {output_path}\")\n',
            '\n',
            '# Hiển thị thử vài dòng để so sánh\n',
            'display(df[[\'text\', \'cleaned_text\', \'label\']].head())'
        ]
    }
]

nb['cells'].extend(cells_to_add)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Appended data processing and saving logic to notebook.')
