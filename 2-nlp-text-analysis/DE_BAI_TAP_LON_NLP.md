
**ĐỀ BÀI TẬP LỚN CUỐI KỲ**

**Phân tích Văn bản & Phân loại Tự động với Machine Learning**

*Thời gian: 3 tuần  |  Tổng điểm: 100 điểm  |  Làm nhóm*

# **1. GIỚI THIỆU ĐỀ TÀI**
Trong bài tập lớn này, sinh viên sẽ thực hiện một pipeline phân tích dữ liệu văn bản hoàn chỉnh, từ thu thập và làm sạch dữ liệu cho đến xây dựng và tối ưu hóa mô hình phân loại văn bản tự động.

## **1.1 Bộ dữ liệu**
Sinh viên sử dụng bộ dữ liệu đánh giá sản phẩm thương mại điện tử tiếng Anh hoặc tiếng Việt (tối thiểu 5.000 mẫu, ít nhất 3 nhãn phân loại). Gợi ý các nguồn dữ liệu:

- [Amazon Product Reviews](https://www.kaggle.com/datasets/saurav9786/amazon-product-reviews) (Kaggle) — Tiếng Anh
- Shopee/[Tiki Reviews Dataset](https://github.com/quangvh23/tiki-dataset-sentiment-classification) — Tiếng Việt
- IMDB Movie Reviews — Tiếng Anh
- Hoặc tự thu thập bằng web scraping (cần giải thích rõ phương pháp)

# **PHẦN A — TIỀN XỬ LÝ & PHÂN TÍCH VĂN BẢN  (20 điểm)**

## **A.1  Khám phá dữ liệu ban đầu**
Tiến hành exploratory data analysis (EDA) cơ bản và trả lời các câu hỏi sau:

### **Câu A1** 
Tải dữ liệu và hiển thị 10 dòng đầu. Mô tả cấu trúc DataFrame: số cột, kiểu dữ liệu từng cột, số lượng mẫu theo từng nhãn. Nhận xét xem dữ liệu có bị mất cân bằng (imbalanced) không? Nếu có, điều này ảnh hưởng như thế nào đến quá trình huấn luyện mô hình?

### **Câu A2** 
Tính toán và hiển thị thống kê về độ dài văn bản (số từ, số ký tự) cho từng nhãn. Sau đó:

- So sánh phân phối độ dài giữa các nhãn. Nhãn nào có văn bản dài hơn?
- Độ dài văn bản có tương quan với nhãn phân loại không? Giải thích tại sao có hoặc không.
## **A.2  Tiền xử lý văn bản** 
Thực hiện pipeline tiền xử lý đầy đủ. Với mỗi bước, sinh viên phải giải thích lý do áp dụng bước đó.

### **Câu A3 — Làm sạch văn bản**
Viết hàm preprocess\_text(text) thực hiện đầy đủ các bước sau:

- Chuyển về chữ thường, loại bỏ HTML tags, URL, ký tự đặc biệt
- Tokenization
- Loại bỏ stopwords
- Stemming hoặc Lemmatization (chọn một, giải thích lý do)

|<p>*Câu hỏi:* </p><p>*(a) Tại sao cần loại bỏ stopwords? Hãy liệt kê 5 stopwords phổ biến và giải thích tại sao chúng không mang nhiều ý nghĩa phân biệt.* </p><p>*(b) So sánh Stemming và Lemmatization: cái nào cho kết quả tốt hơn?*</p>|
| :- |

### **Câu A4 — Đặc trưng văn bản**
Áp dụng hai phương pháp trích xuất đặc trưng và so sánh:

- Bag of Words (CountVectorizer) với max\_features=10000
- TF-IDF (TfidfVectorizer) với max\_features=10000, ngram\_range=(1,2)

|<p>*Câu hỏi:*</p><p>*(a) TF-IDF khác gì so với Bag of Words? Giải thích công thức TF-IDF bằng cách hiểu của bạn..*</p>|
| :- |

## **A.3  Kiểm tra hiểu bài** 
### **Câu A6  — Câu hỏi phân tích**
Một sinh viên khác áp dụng tiền xử lý sau đây. Hãy xác định những vấn đề (nếu có) và đề xuất cách sửa:

|<p>*# Code của sinh viên X — tìm vấn đề*</p><p>vectorizer = TfidfVectorizer()</p><p>X\_train\_vec = vectorizer.fit\_transform(X\_train)</p><p>X\_test\_vec  = vectorizer.fit\_transform(X\_test)   # <-- ?</p>|
| :- |

Ngoài ra, hãy giải thích: Tại sao không được fit vectorizer trên tập test? Hậu quả là gì nếu làm vậy?

# **PHẦN B — TRỰC QUAN HÓA DỮ LIỆU  (20 điểm)**

## **B.1  Biểu đồ thống kê** 
### **Câu B1** 
Vẽ biểu đồ phân phối nhãn (bar chart và pie chart). Áp dụng đúng nguyên tắc thiết kế: tiêu đề rõ ràng, nhãn trục đầy đủ, màu sắc phân biệt, chú thích. Viết nhận xét về dữ liệu.

### **Câu B2**
Vẽ box plot phân phối độ dài văn bản theo từng nhãn trên.

## **B.2  Phân tích từ ngữ** 
### **Câu B4  — Word Cloud**
Tạo word cloud riêng cho từng nhãn (tối thiểu 3 nhãn). Đặt kích thước figure phù hợp, màu nền tương phản. Quan sát và nhận xét: Có sự khác biệt rõ ràng về từ vựng giữa các nhãn không?
# **PHẦN C — XÂY DỰNG MÔ HÌNH CLASSIFICATION  (25 điểm)**

## **C.1  Chuẩn bị và phân chia dữ liệu** 
### **Câu C1**
Phân chia train/validation/test với tỉ lệ 70/10/20. Dùng stratify=y và random\_state cố định. Sau đó:

- In ra số lượng mẫu và phân phối nhãn của từng tập
- Giải thích: Tại sao cần dùng stratify? Điều gì xảy ra nếu không dùng với dữ liệu mất cân bằng?
- Tại sao cần tập validation riêng biệt với tập test?

## **C.2  Huấn luyện mô hình**
Xây dựng tối thiểu 4 mô hình sau. Với mỗi mô hình, dùng TF-IDF features từ Phần A:

|**Mô hình**|**Hyperparameter gợi ý**|**Điểm**|
| :- | :- | :- |
|Naive Bayes|MultinomialNB, alpha={0.1, 0.5, 1.0}|3|
|Logistic Regression|C={0.1, 1, 10}, solver='lbfgs', max\_iter=1000|4|
|SVM|LinearSVC, C={0.1, 1, 10}|4|
|Random Forest|n\_estimators={100,200}, max\_depth={None,10,20}|4|

### **Câu C2 — Câu hỏi hiểu bài về mô hình**
Trả lời ngắn gọn (3–5 câu mỗi câu) cho từng mô hình:

- Logistic Regression: Tham số C kiểm soát điều gì? C lớn hay C nhỏ gây overfitting nhiều hơn?
- SVM: Khái niệm "margin" và "support vectors" là gì? Vì sao SVM phù hợp với dữ liệu văn bản chiều cao?
- Random Forest: Tại sao Random Forest ít bị overfitting hơn một cây quyết định đơn lẻ?

## **C.3  Cross-Validation**
### **Câu C3**
Áp dụng Stratified K-Fold Cross-Validation (k=5) cho tất cả mô hình. Tính mean và std của accuracy trên các fold. Sau đó trả lời:

- Tại sao dùng Stratified K-Fold thay vì K-Fold thông thường?
- Mô hình nào có std cao nhất? Điều này có nghĩa gì?
- Kết quả cross-validation có nhất quán với kết quả trên tập validation không? Nếu không, hãy giải thích nguyên nhân.

# **PHẦN D — ĐÁNH GIÁ & PHÂN TÍCH KẾT QUẢ  (20 điểm)**

## **D.1  Bảng tổng hợp đánh giá**
### **Câu D1**
Lập bảng tổng hợp kết quả của tất cả mô hình trên tập test với đầy đủ các chỉ số:

|**Mô hình**|**Accuracy**|**Precision**|**Recall**|**F1-Score**|
| :- | :- | :- | :- | :- |
|Naive Bayes|?|?|?|?|
|Logistic Regression|?|?|?|?|
|SVM|?|?|?|?|
|Random Forest|?|?|?|?|

Điền kết quả thực nghiệm và dùng macro average cho Precision, Recall, F1-Score.

## **D.2  Phân tích sâu chỉ số**
### **Câu D2 — Phân tích Precision vs Recall**
Với mô hình tốt nhất, phân tích Precision và Recall theo từng nhãn (classification\_report). Trả lời:

- Nhãn nào có Precision cao nhất? Nhãn nào có Recall cao nhất?
- Giả sử đây là hệ thống lọc đánh giá tiêu cực của sản phẩm. Trong bối cảnh này, Precision hay Recall quan trọng hơn? Tại sao? Bạn sẽ điều chỉnh threshold như thế nào?

### **Câu D3  — Phân tích lỗi**
Lấy ngẫu nhiên 10 mẫu bị phân loại sai. Đọc nội dung văn bản và trả lời:

- Các mẫu sai có đặc điểm chung gì? (Ngắn/dài? Mơ hồ? Nhiều nghĩa?)
- Đề xuất ít nhất 1 phương pháp cụ thể để xử lý các trường hợp khó này

### **Câu D4  — Câu hỏi tình huống**

|*Tình huống thực tế: Mô hình của bạn đạt Accuracy = 85% trên tập test. Khách hàng nói: 'Accuracy 85% là đủ tốt để triển khai lên production.' Bạn đồng ý không? Trình bày lập luận của bạn, xem xét các yếu tố: phân phối nhãn, loại lỗi nào nguy hiểm hơn, chi phí của False Positive vs False Negative, và các chỉ số bổ sung cần kiểm tra trước khi triển khai.*|
| :- |

# **PHẦN E — TỐI ƯU HÓA & CẢI TIẾN MÔ HÌNH  (15 điểm)**

## **E.1  Hyperparameter Tuning**
### **Câu E1**
Áp dụng GridSearchCV hoặc RandomizedSearchCV cho ít nhất 2 mô hình tốt nhất từ Phần C. Ghi lại:

- Không gian tham số đã thử nghiệm (ít nhất 3 tham số, mỗi tham số ít nhất 3 giá trị)
- Best parameters tìm được
- Cải thiện so với baseline (điểm trước và sau tuning)

### **Câu E2** 
Trả lời các câu hỏi về quá trình tuning:

- GridSearchCV và RandomizedSearchCV khác nhau như thế nào? Khi nào nên dùng cái nào?
- Tại sao phải dùng cross-validation trong GridSearchCV thay vì evaluate trực tiếp trên tập test?
- Bạn có nhận thấy hiện tượng "diminishing returns" (cải thiện ít dần) khi tuning không? Giải thích nguyên nhân.

## **E.2  Kỹ thuật cải tiến nâng cao**
### **Câu E3 — Chọn và triển khai ít nhất 1 kỹ thuật**
Chọn ít nhất một trong các kỹ thuật sau và triển khai, so sánh với baseline:

- Xử lý mất cân bằng: SMOTE, class\_weight='balanced', hoặc oversampling/undersampling
- Ensemble: Voting Classifier (soft/hard voting) hoặc Stacking
- Feature engineering: Thêm đặc trưng thủ công (độ dài, số dấu chấm than, tỉ lệ uppercase...)
- Dimensionality reduction: TruncatedSVD (LSA) trước khi đưa vào mô hình

Với kỹ thuật đã chọn: giải thích nguyên lý hoạt động, lý do chọn kỹ thuật này cho dữ liệu của bạn, và so sánh kết quả trước/sau.

### **Câu E4 — Phản tư và đề xuất**
Viết một đoạn phân tích (300–400 từ) trả lời:

- Nếu có thêm 2 tuần và tài nguyên không giới hạn, bạn sẽ thử những hướng nào? (Gợi ý: Word2Vec/BERT embeddings, deep learning, thu thập thêm dữ liệu...)
- Bài học quan trọng nhất bạn rút ra từ dự án này là gì?

# **TIÊU CHÍ CHẤM ĐIỂM & YÊU CẦU NỘP BÀI**

## **7.1  Phân bổ điểm**

|**Phần**|**Nội dung chính**|**Điểm**|
| :- | :- | :- |
|Phần A (20đ)|Tiền xử lý & Phân tích văn bản|20|
|Phần B (20đ)|Trực quan hóa dữ liệu|20|
|Phần C (25đ)|Xây dựng mô hình Classification|25|
|Phần D (20đ)|Đánh giá & Phân tích kết quả|20|
|Phần E (15đ)|Tối ưu hóa & Cải tiến mô hình|15|
|Tổng||100|

## **7.2  Tiêu chí đánh giá chất lượng**

|**Tiêu chí**|**Mô tả**|**Điểm tối đa**|**Ghi chú**|
| :- | :- | :- | :- |
|Code chất lượng|Sạch, đúng convention|20||
|Phân tích sâu|Trả lời câu hỏi, có lập luận|30|Bắt buộc|
|Thực nghiệm|Chạy đúng, kết quả hợp lý|30||
|Báo cáo|Trình bày rõ ràng, đầy đủ|20|PDF/DOCX|

## **7.3  Yêu cầu nộp bài**
Sinh viên nộp một file .zip với cấu trúc sau:

- Ten\_nhom/
  - notebook.ipynb — Jupyter Notebook đầy đủ với output
  - report.pdf — Báo cáo
  - data/ — Dữ liệu hoặc script thu thập (nếu dữ liệu > 50MB thì nộp link Google Drive)

Deadline: Cuối tuần thứ 3 kể từ ngày phát đề, trước 23:59.

## **7.4  Quy định về học thuật**

|*⚠️  Nghiêm cấm sao chép code và kết quả của nhau. Sinh viên được phép tham khảo tài liệu, Stack Overflow, và sử dụng AI để hỗ trợ — nhưng phải hiểu và có thể giải thích mọi dòng code trong bài nộp. Giảng viên có thể yêu cầu vấn đáp bất kỳ phần nào.*|
| :- |

# **TÀI LIỆU THAM KHẢO GỢI Ý**

**Thư viện Python:**

- scikit-learn: https://scikit-learn.org/stable/user\_guide.html
- NLTK / spaCy — xử lý ngôn ngữ tự nhiên
- matplotlib / seaborn / wordcloud — trực quan hóa
- pandas / numpy — xử lý dữ liệu

**Khái niệm cần nắm vững:**

- Text preprocessing pipeline (tokenize, stopwords, stemming/lemmatization)
- TF-IDF và Bag of Words representation
- Evaluation metrics: Accuracy, Precision, Recall, F1, AUC-ROC
- Cross-validation, GridSearchCV, bias-variance tradeoff


