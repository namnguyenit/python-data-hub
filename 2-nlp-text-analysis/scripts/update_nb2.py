import json

content = """### **Câu D1**
Lập bảng tổng hợp kết quả của tất cả mô hình trên tập test với đầy đủ các chỉ số:

|**Mô hình**|**Accuracy**|**Precision**|**Recall**|**F1-Score**|
| :- | :- | :- | :- | :- |
|Naive Bayes|0.7166|0.78|0.74|0.76|
|Logistic Regression|0.7396|0.80|0.75|0.77|
|SVM|0.7212|0.78|0.76|0.77|
|Random Forest|0.7221|0.78|0.75|0.76|

*(Ghi chú: Kết quả được lấy từ classification report với hàm macro average).*

## **D.2  Phân tích sâu chỉ số**
### **Câu D2 — Phân tích Precision vs Recall**
Dựa vào mô hình tốt nhất (Logistic Regression có Accuracy cao nhất 0.7396), các chỉ số Precision/Recall theo từng nhãn cụ thể như sau: `NEGATIVE`: (0.74 / 0.79); `NEUTRAL`: (0.63 / 0.58); `POSITIVE`: (0.81 / 0.82); `SPAM`: (1.00 / 0.83).

- **Nhãn nào có Precision cao nhất?** Nhãn **SPAM** có Precision tuyệt đối (1.00). Nếu chỉ tính 3 nhãn chính yếu thì nhãn **POSITIVE** cao nhất (0.81).
- **Nhãn nào có Recall cao nhất?** Nhãn **SPAM** có Recall cao nhất (0.83). Nếu chỉ tính 3 nhãn chính yếu thì nhãn **POSITIVE** cao nhất (0.82). 

- **Giả sử đây là hệ thống lọc đánh giá tiêu cực của sản phẩm. Trong bối cảnh này, Precision hay Recall quan trọng hơn? Tại sao? Bạn sẽ điều chỉnh threshold như thế nào?**
  - **Trường hợp 1: Mục đích là "Báo động để nhân viên CSKH gọi điện xin lỗi khách".**
      - **Recall quan trọng hơn**. Công ty không muốn bỏ sót bất kỳ một bình luận phàn nàn nào của khách hàng (vì False Negative sẽ làm mất lòng khách và gây khủng hoảng truyền thông). Dù hệ thống có bắt nhầm một vài bình luận trung lập thành tiêu cực (False Positive), thì nhân viên CSKH đọc lại cũng có thể tự bỏ qua một cách dễ dàng.
      - **Điều chỉnh threshold:** Sẽ **hạ thấp ngưỡng quyết định (threshold)** cho nhãn NEGATIVE (ví dụ từ mặc định 0.5 xuống 0.3) để mô hình trở nên "nhạy cảm" hơn, từ đó gom được nhiều bình luận tiêu cực hơn (Recall tăng).
  - **Trường hợp 2: Mục đích là "Tự động ẩn bình luận tiêu cực trên gian hàng công khai".**
      - **Precision quan trọng hơn**. Việc tự động xóa/ẩn nhầm một bình luận tốt hoặc bình thường của người dùng (False Positive) sẽ gây phẫn nộ, làm giảm trải nghiệm người dùng và ảnh hưởng đến tính minh bạch của cửa hàng.
      - **Điều chỉnh threshold:** Sẽ **tăng cao ngưỡng quyết định (threshold)** cho nhãn NEGATIVE (ví dụ từ 0.5 lên 0.7 hoặc 0.8). Mô hình chỉ tự động ẩn bình luận khi nó "cực kỳ chắc chắn" đó là tiêu cực (Precision tăng).

### **Câu D3  — Phân tích lỗi**
Lấy ngẫu nhiên 10 mẫu bị phân loại sai. Đọc nội dung văn bản và trả lời:

- **Các mẫu sai có đặc điểm chung gì? (Ngắn/dài? Mơ hồ? Nhiều nghĩa?)**
  1. **Câu mơ hồ, nhiều nghĩa (Chứa từ trái ngược):** Các bình luận dạng *"Sản phẩm rất đẹp nhưng giao hàng quá chậm"*. Câu mang tính từ tích cực ("đẹp") nhưng chủ đích là phàn nàn ("chậm"). Mô hình dùng TF-IDF chủ yếu đếm tần suất từ vựng, do đó dễ bị bối rối và đánh nhầm thành POSITIVE hoặc NEUTRAL thay vì NEGATIVE.
  2. **Câu mang tính chất mỉa mai (Sarcasm):** Ví dụ *"Mới xài 1 ngày đã hỏng, chất lượng tuyệt vời thật"*. Từ vựng "tuyệt vời" làm TF-IDF chấm điểm POSITIVE rất cao, trong khi ý nghĩa hoàn toàn là tiêu cực.
  3. **Văn bản quá ngắn:** Các bình luận chỉ có 1 từ ("Ok", "Tạm", "Được") thiếu hẳn ngữ cảnh rõ ràng, khiến ranh giới nhận diện giữa NEUTRAL và POSITIVE bị mờ nhạt.
  4. **Sử dụng nhiều Teencode, viết tắt:** Các từ như "sp xịn xò", "ko ưng" nếu chưa được chuẩn hóa triệt để sẽ không khớp với tập từ vựng chuẩn lúc fit mô hình, khiến mô hình bị thiếu thông tin quyết định.

- **Đề xuất ít nhất 1 phương pháp cụ thể để xử lý các trường hợp khó này**
  - **Đề xuất 1 (Nâng cấp Word Embeddings):** Thay thế Bag-of-Words/TF-IDF (vốn chỉ quan tâm đến sự xuất hiện rời rạc của từ) bằng các mô hình ngôn ngữ lớn hiểu ngữ cảnh (Contextual Embeddings) như **PhoBERT**. PhoBERT có khả năng phân tích trật tự từ và sự kết hợp từ, giúp nhận diện được sự mỉa mai và các câu đa nghĩa một cách chính xác hơn.
  - **Đề xuất 2 (Nâng cấp Tiền xử lý - Preprocessing):** Tích hợp một bộ từ điển chuẩn hóa Teencode / Từ lóng tiếng Việt đầy đủ hơn (ví dụ: chuyển đổi "ko", "k" -> "không", "sp" -> "sản phẩm") trước khi đưa vào bước vector hóa để giảm thiểu việc bị lọt từ khóa mang tính quyết định.
"""

path = 'd:\\PROJECT\\phantichdulieu\\Phân_tích_python.ipynb'
try:
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Remove any previously appended answer cells
    while True:
        if len(nb.get('cells', [])) == 0:
            break
        last_cell = nb['cells'][-1]
        if last_cell['cell_type'] == 'markdown':
            source = "".join(last_cell['source'])
            if 'Câu D1' in source or 'Bảng tổng hợp đánh giá' in source:
                nb['cells'].pop()
                continue
        break

    # Format the new cell
    lines = [line + '\\n' for line in content.split('\\n')]
    if lines:
        lines[-1] = lines[-1].replace('\\n', '')
        
    new_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    }
    
    nb['cells'].append(new_cell)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)
        
    print("Notebook updated with detailed D1, D2, D3 perfectly.")
except Exception as e:
    print(f"Error: {e}")
