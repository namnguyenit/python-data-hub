import json
from collections import Counter

def analyze_jsonl(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
            
    print("--- Tổng quan ---")
    print(f"Tổng số bản ghi: {len(data)}")
    
    labels = [d.get('label') for d in data]
    print("\n--- Nhãn (Label) ---")
    for k, v in Counter(labels).most_common():
        print(f"{k}: {v}")
    
    ratings = [d.get('rating') for d in data]
    print("\n--- Điểm số (Rating) ---")
    for k, v in Counter(ratings).most_common():
        print(f"{k} sao: {v}")
    
    review_lens = [len(d.get('review', '')) for d in data]
    word_counts = [len(d.get('review', '').split()) for d in data]
    
    print("\n--- Độ dài văn bản (Review length) ---")
    print(f"Ký tự - Min: {min(review_lens)}, Max: {max(review_lens)}, Trung bình: {sum(review_lens)/len(review_lens):.2f}")
    print(f"Số từ - Min: {min(word_counts)}, Max: {max(word_counts)}, Trung bình: {sum(word_counts)/len(word_counts):.2f}")
    
    print("\n--- Một số mẫu (Samples) ---")
    for i in range(3):
        print(f"\nMẫu {i+1}:")
        print(f"Label: {data[i].get('label')}, Rating: {data[i].get('rating')}")
        print(f"Review: {data[i].get('review')}")

if __name__ == '__main__':
    filepath = r'd:\PROJECT\phantichdulieu\aug_unaccented_reviews.jsonl'
    analyze_jsonl(filepath)
