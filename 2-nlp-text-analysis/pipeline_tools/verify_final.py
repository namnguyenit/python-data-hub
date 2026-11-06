import csv
from collections import Counter

def check_balance(filepath):
    labels = Counter()
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels[row['label']] += 1
            
    print("--- KIỂM TRA SỐ LƯỢNG MỖI NHÃN ---")
    for l, c in labels.most_common():
        print(f"{l}: {c:,} mẫu")

if __name__ == '__main__':
    check_balance(r'd:\PROJECT\phantichdulieu\final_balanced_dataset.csv')
