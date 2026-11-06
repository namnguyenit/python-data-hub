import os
import time
import numpy as np

start = time.time()
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "server.log")
with open(file_path, "r",encoding="utf-8") as f:
    lines = f.readlines()
error = 0
info = 0
warning = 0
for line in lines:
    if line.find("ERROR") != -1:
        error += 1
    elif line.find("INFO") != -1:
        info += 1
    elif line.find("WARNING") != -1:
        warning += 1
logs=[]
for line in lines:
    line = line.strip()
    logs.append(line.split(" ",3)[3])
count_log = {}

for log in logs:
    if log in count_log:
        count_log[log] +=1
    else:
        count_log[log] =1
list_max_log = []
for key, item in count_log.items():
    if item == max(count_log.values()):
        list_max_log.append(key)
print(list_max_log)

print("=== BÁO CÁO LOG ===")
print("Tổng số dòng: ", len(lines))
print("ERROR: ", error)
print("INFO:", info)
print("WARNING", warning)
print("Lỗi phổ biến nhất:")
max_log = max(count_log.values())
for item in list_max_log:
    print(item+f" ({max_log} lần)")
end = time.time()

print("Thời gian chạy:", end - start, "giây")

report_path = os.path.join(base_dir, "report.txt")
with open(report_path, "w", encoding="utf-8") as report_file:
    report_file.write("=== BÁO CÁO LOG ===\n")
    report_file.write(f"Tổng số dòng: {len(lines)}\n")
    report_file.write(f"ERROR: {error}\n")
    report_file.write(f"INFO: {info}\n")
    report_file.write(f"WARNING: {warning}\n")
    report_file.write("Lỗi phổ biến nhất:\n")
    for item in list_max_log:
        report_file.write(f"{item} ({max_log} lần)\n")
    report_file.write(f"Thời gian chạy: {end - start} giây\n")

