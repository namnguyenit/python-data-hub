import json

content = """### **D.1 Bảng tổng hợp đánh giá (Câu D1)**
Dưới đây là bảng kết quả các chỉ số trên **tập Validation**:

| Mô hình | Accuracy |
| :--- | :--- |
| **Naive Bayes (Cross-Validation Mean)** | 0.7118 (71.18%) |
| **Logistic Regression** | 0.7396 (73.96%) |
| **SVM** | 0.7212 (72.12%) |
| **Random Forest** | 0.7221 (72.21%) |

*(Lưu ý: Logistic Regression là mô hình mang lại kết quả tổng thể tốt nhất trên tập validation với Accuracy 73.96%)*

---

### **D.2 Phân tích sâu chỉ số**

#### **Câu D2 — Phân tích Precision vs Recall**
Lấy báo cáo phân loại (Classification Report) của **SVM** theo từng nhãn như sau:
*   `POSITIVE`: Precision = 0.79, Recall = 0.82
*   `NEGATIVE`: Precision = 0.73, Recall = 0.76
*   `NEUTRAL`: Precision = 0.60, Recall = 0.55
*   `SPAM`: Precision = **1.00**, Recall = **0.92**

**Trả lời câu hỏi:**
*   **Nhãn nào có Precision cao nhất?** Nhãn **SPAM** (1.00). (Tuy nhiên nếu loại trừ nhãn thiểu số SPAM, nhãn POSITIVE có Precision cao nhất là 0.79).
*   **Nhãn nào có Recall cao nhất?** Nhãn **SPAM** (0.92). (Nếu loại trừ SPAM, nhãn POSITIVE có Recall cao nhất là 0.82).

*   **Giả sử đây là hệ thống lọc đánh giá tiêu cực. Trong bối cảnh này, Precision hay Recall quan trọng hơn? Tại sao? Bạn sẽ điều chỉnh threshold như thế nào?**
    *   **Nếu mục tiêu là "Cảnh báo CSKH" (Customer Service Alert):** **Recall quan trọng hơn**. Chúng ta không muốn bỏ sót bất kỳ một khách hàng nào đang tức giận hoặc phàn nàn về sản phẩm (False Negative chi phí rất cao). Dù hệ thống có bắt nhầm một vài bình luận trung lập thành tiêu cực (False Positive) thì nhân viên CSKH vẫn có thể bỏ qua sau khi đọc. 
        *   *Điều chỉnh threshold:* Sẽ **hạ thấp ngưỡng (threshold) phân loại cho nhãn NEGATIVE** (ví dụ từ 0.5 xuống 0.3) để mô hình nhạy cảm hơn và bắt được nhiều bình luận tiêu cực hơn.
    *   **Nếu mục tiêu là "Tự động ẩn bình luận tiêu cực trên Web":** **Precision quan trọng hơn**. Nếu hệ thống ẩn nhầm một đánh giá Tích cực hoặc Trung lập chỉ vì mô hình dự đoán sai (False Positive), trải nghiệm người dùng và tính minh bạch của cửa hàng sẽ bị ảnh hưởng nghiêm trọng. 
        *   *Điều chỉnh threshold:* Sẽ **nâng cao ngưỡng (threshold) phân loại cho nhãn NEGATIVE** (ví dụ từ 0.5 lên 0.7) để mô hình chỉ đánh dấu tiêu cực khi nó cực kỳ "chắc chắn".

#### **Câu D3 — Phân tích lỗi**
Dựa vào các mẫu bị phân loại sai, ta có thể rút ra nhận xét:

*   **Các mẫu sai có đặc điểm chung gì?**
    1.  **Chứa tính từ mang nhiều nghĩa hoặc đa cảm xúc (Mơ hồ):** Các câu như *"Sản phẩm đẹp nhưng giao hàng quá chậm"* vừa có từ tích cực ("đẹp") vừa có từ tiêu cực ("chậm"). Mô hình TF-IDF đếm tần suất từ nên dễ bối rối và gán nhãn sai thành NEUTRAL hoặc POSITIVE.
    2.  **Sử dụng Teencode, viết tắt, hoặc sai chính tả:** Các từ lóng ("sp xịn xò", "ko ưng") không có trong tập từ vựng chuẩn (Bag of Words/TF-IDF) nên mô hình bỏ qua, dẫn đến việc thiếu cơ sở dự đoán đúng.
    3.  **Văn bản quá ngắn:** Bình luận chỉ có 1-2 từ (ví dụ: "Ok", "Tạm") thiếu hẳn ngữ cảnh khiến việc phân tách giữa NEUTRAL và POSITIVE bị lẫn lộn.
    4.  **Mỉa mai (Sarcasm):** Ví dụ *"Tuyệt vời, mới dùng 1 ngày đã hỏng"*. Mô hình TF-IDF thấy từ "Tuyệt vời" sẽ cho điểm POSITIVE rất cao nhưng ý nghĩa thực tế lại là NEGATIVE.

*   **Đề xuất ít nhất 1 phương pháp cụ thể để xử lý các trường hợp khó này:**
    *   **Sử dụng mô hình Word Embeddings theo ngữ cảnh (Contextual Embeddings) như PhoBERT:** Thay vì dùng TF-IDF (chỉ quan tâm tới sự xuất hiện rời rạc của từ), PhoBERT có khả năng hiểu ngữ cảnh của toàn bộ câu. Nó có thể hiểu được chữ "Tuyệt vời" đặt cạnh "đã hỏng" là mang ý nghĩa mỉa mai, và có thể hiểu các câu đánh giá phức tạp, đa chiều.
    *   **Chuẩn hoá Teencode chuyên sâu:** Tích hợp một từ điển chuyển đổi Teencode/Từ viết tắt tiếng Việt mạnh mẽ hơn trong bước tiền xử lý trước khi đưa vào mô hình.
"""

path = 'd:\\PROJECT\\phantichdulieu\\Phân_tích_python.ipynb'
try:
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Remove any previously appended answer cells
    while True:
        if len(nb['cells']) == 0:
            break
        last_cell = nb['cells'][-1]
        if last_cell['cell_type'] == 'markdown':
            source = "".join(last_cell['source'])
            if 'Bảng tổng hợp đánh giá' in source:
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
        
    print("Notebook fixed successfully.")
except Exception as e:
    print(f"Error: {e}")
