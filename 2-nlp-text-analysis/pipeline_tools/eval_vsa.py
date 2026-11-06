import pandas as pd
import sys

def evaluate_vsa(filepath):
    try:
        df = pd.read_csv(filepath)
        print("--- THỐNG KÊ DATASET ---")
        print(f"Tổng số dòng: {len(df):,}")
        print(f"Số cột: {len(df.columns)} ({', '.join(df.columns)})")
        
        print("\n--- PHÂN BỔ NHÃN (RATING) ---")
        print(df['Rating'].value_counts(dropna=False).to_string())
        
        print("\n--- KIỂM TRA NULL ---")
        print(df.isnull().sum().to_string())
        
        print("\n--- CHIỀU DÀI TRUNG BÌNH CỦA COMMENT ---")
        df['length'] = df['Comment'].astype(str).apply(len)
        print(f"Ngắn nhất: {df['length'].min()} ký tự")
        print(f"Dài nhất: {df['length'].max()} ký tự")
        print(f"Trung bình: {df['length'].mean():.2f} ký tự")
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    evaluate_vsa(r'd:\PROJECT\phantichdulieu\vsa_food_rv_train.csv')
