import json
import csv
import os

def jsonl_to_csv(jsonl_path, csv_path):
    # Read the JSONL file
    data = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
                
    if not data:
        print("File JSONL trống.")
        return

    # Extract headers (keys) from the first object, or union of all keys
    headers = list(data[0].keys())
    
    # Ensure standard order if possible
    standard_headers = ['id', 'review', 'rating', 'label']
    if all(h in headers for h in standard_headers):
        headers = standard_headers

    # Write to CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
    print(f"Chuyển đổi thành công! Đã lưu file tại: {csv_path}")

if __name__ == '__main__':
    base_dir = r'd:\PROJECT\phantichdulieu'
    jsonl_file = os.path.join(base_dir, 'aug_unaccented_reviews.jsonl')
    csv_file = os.path.join(base_dir, 'aug_unaccented_reviews.csv')
    
    jsonl_to_csv(jsonl_file, csv_file)
