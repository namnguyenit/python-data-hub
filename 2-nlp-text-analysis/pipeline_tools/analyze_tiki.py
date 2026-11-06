import os
from collections import Counter

def analyze_tiki_data(folder_path):
    print(f"--- PHÂN TÍCH THƯ MỤC {os.path.basename(folder_path)} ---")
    total_records = 0
    ratings_counter = Counter()
    
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    print(f"Số lượng file (chuyên mục): {len(files)}")
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 8:
                    total_records += 1
                    rating = parts[2]
                    ratings_counter[rating] += 1
                    
    print(f"Tổng số lượng đánh giá: {total_records:,}")
    print("Phân bổ điểm số (Rating từ 0-100):")
    for r, count in sorted(ratings_counter.items(), key=lambda x: int(x[0]) if x[0].isdigit() else -1):
        print(f"  Điểm {r}: {count:,} ({count/total_records*100:.2f}%)")
    print("\n")

if __name__ == '__main__':
    base_dir = r'd:\PROJECT\phantichdulieu'
    analyze_tiki_data(os.path.join(base_dir, '1a3'))
    analyze_tiki_data(os.path.join(base_dir, '1a6'))
