import csv

def inspect_v3(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            print(f"Header v3.csv: {header}")
            
            # Read first 5 rows
            for i, row in enumerate(reader):
                if i < 5:
                    print(f"Row {i+1}: {row}")
                else:
                    break
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    inspect_v3(r'd:\PROJECT\phantichdulieu\v3.csv')
