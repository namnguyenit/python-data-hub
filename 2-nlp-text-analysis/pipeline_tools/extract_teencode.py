import csv
from collections import Counter
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Đọc dữ liệu gốc
data_path = "d:/PROJECT/phantichdulieu/final_balanced_dataset.csv"
try:
    word_counter = Counter()
    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get('text', '')
            word_counter.update(text.lower().split())

    vietnamese_vowels_accents = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
    potential_teencodes = []

    for word, count in word_counter.most_common(1500):
        if len(word) < 2 and word not in ["k", "m", "t", "j", "v", "z", "q"]:
            continue
        has_accent = any(char in vietnamese_vowels_accents for char in word)
        if not has_accent:
            potential_teencodes.append((word, count))

    print("TOP POTENTIAL TEENCODE WORDS:")
    for w, c in potential_teencodes[:150]:
        print(f"{w}: {c}")

except Exception as e:
    print(f"Lỗi: {e}")
