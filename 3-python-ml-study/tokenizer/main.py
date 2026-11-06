text = "UBND TP Hà Nội đã ban hành quyết định 123.45 về việc triển khai dẹp bỏ 231,45 chợ cóc, điểm kinh doanh tự phát trên địa bàn. Tuy nhiên, nhiều chợ cóc hoạt động trái phép ở nội đô chưa có tên trong danh mục này."
moi= text.split()
result=[]
for w in moi:
    if w.endswith(",") or w.endswith("."):
        result += [w[:-1], w[-1]]
    else:
        result += [w]
print(result)
