import csv
import sys

def count_labels(filepath):
    csv.field_size_limit(sys.maxsize)
    count_0 = 0
    count_1 = 0
    other = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # We can't always trust the CSV to be perfectly formatted, so let's just use string parsing or csv reader.
            # Using basic string splitting might be faster but less safe if texts contain commas.
            # Let's use csv reader.
            reader = csv.reader(f)
            header = next(reader, None)
            
            for row in reader:
                if len(row) >= 2:
                    label = row[1].strip()
                    if label == '0':
                        count_0 += 1
                    elif label == '1':
                        count_1 += 1
                    else:
                        other += 1
    except Exception as e:
        print(f"Error: {e}")
        
    print(f"Nhãn 0 (Clean): {count_0:,}")
    print(f"Nhãn 1 (Toxic): {count_1:,}")
    print(f"Khác: {other:,}")
    
    total = count_0 + count_1 + other
    if total > 0:
        print(f"Tỉ lệ Nhãn 0: {count_0/total*100:.2f}%")
        print(f"Tỉ lệ Nhãn 1: {count_1/total*100:.2f}%")

if __name__ == '__main__':
    count_labels('data.csv')
