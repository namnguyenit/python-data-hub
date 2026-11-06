import csv
import sys
from collections import Counter

def evaluate_data(filepath):
    csv.field_size_limit(sys.maxsize)
    total_rows = 0
    labels_counter = Counter()
    ratings_counter = Counter()
    lengths = []
    
    print("--- ĐANG ĐỌC DATASET ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            
            for row in reader:
                if len(row) >= 3:
                    total_rows += 1
                    comment = row[0].strip()
                    label = row[1].strip()
                    rate = row[2].strip()
                    
                    labels_counter[label] += 1
                    ratings_counter[rate] += 1
                    lengths.append(len(comment))
                    
        print(f"Tổng số đánh giá: {total_rows:,}")
        
        print("\n--- PHÂN BỔ NHÃN (LABEL) ---")
        for l, c in labels_counter.most_common():
            print(f"Nhãn {l}: {c:,} ({c/total_rows*100:.2f}%)")
            
        print("\n--- PHÂN BỔ ĐIỂM SỐ (RATING) ---")
        for r, c in sorted(ratings_counter.items()):
            print(f"Rating {r}: {c:,} ({c/total_rows*100:.2f}%)")
            
        print("\n--- CHIỀU DÀI TRUNG BÌNH CỦA COMMENT ---")
        if lengths:
            print(f"Ngắn nhất: {min(lengths)} ký tự")
            print(f"Dài nhất: {max(lengths)} ký tự")
            print(f"Trung bình: {sum(lengths)/len(lengths):.2f} ký tự")
            
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    evaluate_data(r'd:\PROJECT\phantichdulieu\data - data.csv')
