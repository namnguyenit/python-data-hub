import time
start = time.time()
report = {
    'ERROR': 0,
    'INFO' :0,
    'WARNING':0
}
error = {
}
top_error=''
time_top_error=0
total_line=0
with open('./server.log','r') as server_log:
    data = server_log.readlines()
    lenght = len(data)
    total_line = lenght
    for i in range(lenght):
        # print(data[i].split(' ',3)[2])
        splitData = data[i].split(' ',3)
        type = splitData[2]
        errorName =splitData[3].strip()
        # print('---------------------')
        # print(errorName)
        # print(type)
        if(type == 'ERROR'):
            report['ERROR'] +=1
            if errorName in error:
                error[errorName]  +=1
            else:
                error[errorName] = 1
        elif(type == 'INFO'):
            report['INFO'] +=1
        elif(type == 'WARNING'):
            report['WARNING'] +=1

    top_error = max(error, key=error.get)
    time_top_error = error[top_error]
print(top_error)
print(time_top_error)
print(report)
print(error)
with open('./report.txt','w',encoding='utf-8') as server_log:
    server_log.write('=== BÁO CÁO LOG ===\n')
    server_log.write(f'Tổng số dòng: {total_line}\n')
    server_log.write(f'- ERROR: {report["ERROR"]}\n')
    server_log.write(f'- INFO: {report["INFO"]}\n')
    server_log.write(f'- WARNING: {report["WARNING"]}\n')
    server_log.write(f'Lỗi phổ biến nhất: {top_error} ({time_top_error} lần)\n')