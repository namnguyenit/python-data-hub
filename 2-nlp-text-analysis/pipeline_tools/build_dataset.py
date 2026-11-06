import csv
import os
import random
import sys

def clean_text(text):
    # Remove newlines and tabs to keep csv clean
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', '')
    # Remove multiple spaces
    return ' '.join(text.split())

def build_dataset():
    csv.field_size_limit(sys.maxsize)
    dataset = []
    
    # 1. READ data - data.csv
    data_csv_path = r'd:\PROJECT\phantichdulieu\data - data.csv'
    pos_count = 0
    target_pos = 7300
    
    print("Đang lấy dữ liệu từ data - data.csv...")
    with open(data_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                text = clean_text(row[0])
                label = row[1].strip()
                if not text: continue
                
                if label == 'NEG':
                    dataset.append({'text': text, 'label': 'NEGATIVE'})
                elif label == 'NEU':
                    dataset.append({'text': text, 'label': 'NEUTRAL'})
                elif label == 'POS' and pos_count < target_pos:
                    dataset.append({'text': text, 'label': 'POSITIVE'})
                    pos_count += 1

    # 2. READ aug_unaccented_reviews.csv
    aug_path = r'd:\PROJECT\phantichdulieu\aug_unaccented_reviews.csv'
    print("Đang lấy dữ liệu từ aug_unaccented_reviews.csv...")
    if os.path.exists(aug_path):
        with open(aug_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = clean_text(row.get('review', ''))
                label = row.get('label', '').strip()
                if not text: continue
                
                if label == 'negative':
                    dataset.append({'text': text, 'label': 'NEGATIVE'})
                elif label == 'positive':
                    dataset.append({'text': text, 'label': 'POSITIVE'})

    # 3. READ 1a3 for more NEUTRAL
    tiki_path = r'd:\PROJECT\phantichdulieu\1a3'
    print("Đang lấy dữ liệu NEUTRAL từ Tiki (1a3)...")
    if os.path.exists(tiki_path):
        for file in os.listdir(tiki_path):
            if file.endswith('.txt'):
                with open(os.path.join(tiki_path, file), 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split('\t')
                        if len(parts) >= 8:
                            rating = parts[2].strip()
                            if rating == '60': # Neutral rating
                                text = clean_text(parts[7])
                                dataset.append({'text': text, 'label': 'NEUTRAL'})

    # 4. READ v3.csv for SPAM
    v3_path = r'd:\PROJECT\phantichdulieu\v3.csv'
    spam_keywords = ['nhận xu', 'hình ảnh mang tính', 'minh hoạ', 'minh họa', 'video không liên quan', 'chống trôi', 'lấy xu', 'chỉ mang tính chất']
    spam_count = 0
    target_spam = 7300
    
    print("Đang lọc SPAM từ v3.csv...")
    if os.path.exists(v3_path):
        with open(v3_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t') # It seems to be tab separated from my inspection
            next(reader, None)
            for row in reader:
                if len(row) >= 7:
                    text = clean_text(row[6])
                    text_lower = text.lower()
                    if any(kw in text_lower for kw in spam_keywords):
                        dataset.append({'text': text, 'label': 'SPAM'})
                        spam_count += 1
                        if spam_count >= target_spam:
                            break
                            
    # Fallback if v3 was strictly comma separated with \t inside strings
    # We will just re-read if spam_count is 0
    if spam_count == 0 and os.path.exists(v3_path):
        with open(v3_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                # find the column that might have the comment, usually the longest one or just join them
                text = clean_text(" ".join(row))
                text_lower = text.lower()
                if any(kw in text_lower for kw in spam_keywords):
                    dataset.append({'text': text, 'label': 'SPAM'})
                    spam_count += 1
                    if spam_count >= target_spam:
                        break

    # Shuffle dataset
    random.seed(42)
    random.shuffle(dataset)
    
    # Save to CSV
    output_path = r'd:\PROJECT\phantichdulieu\final_balanced_dataset.csv'
    print(f"Đang lưu {len(dataset)} dòng ra {output_path}...")
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'label'])
        writer.writeheader()
        writer.writerows(dataset)
        
    print("Hoàn thành!")

if __name__ == '__main__':
    build_dataset()
