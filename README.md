# 🚀 Python Data Hub: Web Scraping, NLP Text Analytics & Machine Learning

Chào mừng bạn đến với **Python Data Hub** — kho lưu trữ hợp nhất chuyên nghiệp các dự án Python phục vụ:
1. **Web Scraping & Data Engineering**: Hệ thống cào dữ liệu bóng đá Ngoại Hạng Anh (EPL) từ FBref và FootballTransfers lưu trữ vào MySQL.
2. **NLP & Text Analytics**: Pipeline xử lý ngôn ngữ tự nhiên phân loại đánh giá sản phẩm thương mại điện tử tiếng Việt (Xử lý teencode, loại bỏ stopwords, trích xuất đặc trưng và huấn luyện mô hình Machine Learning).
3. **Python & Machine Learning Foundations**: Bài tập và tài liệu thực hành cốt lõi về NumPy, Matplotlib, Scikit-learn và Tokenizer.

---

## 📁 Cấu trúc thư mục (Architecture)

```text
python-data-hub/
├── 1-premier-league-scraper/        # Web Crawler bóng đá Ngoại Hạng Anh
│   ├── fbref.py                    # Cào chỉ số cầu thủ và bảng xếp hạng từ FBref
│   ├── footballtransfers.py        # Cào giá trị chuyển nhượng từ FootballTransfers
│   ├── mysql_db.py                 # Kết nối và lưu trữ dữ liệu MySQL
│   ├── http_utils.py               # Quản lý HTTP requests, headers & retry
│   ├── config.py                   # Đọc biến môi trường và thiết lập
│   ├── main.py                     # Entrypoint điều phối luồng cào dữ liệu
│   └── requirements.txt            # Thư viện cho crawler (Selenium, BeautifulSoup4, PyMySQL)
│
├── 2-nlp-text-analysis/            # Phân tích văn bản tiếng Việt & NLP Pipeline
│   ├── notebooks/
│   │   └── Phan_tich_van_ban_NLP.ipynb # Jupyter Notebook hoàn chỉnh phân tích dữ liệu & mô hình
│   ├── datasets/                   # Bộ dữ liệu đánh giá sản phẩm (CSV, JSONL)
│   ├── dictionaries/               # Từ điển chuẩn hóa Teencode và danh sách Stopwords
│   ├── raw_data/                   # Dữ liệu phân loại theo ngành hàng (Mỹ phẩm, Đồ dùng, v.v.)
│   ├── scripts/                    # Script tiền xử lý và trích xuất dữ liệu
│   └── pipeline_tools/             # Bộ script chuẩn hóa, tích hợp VnCoreNLP & đánh giá
│
└── 3-python-ml-study/              # Bài tập & kiến thức nền tảng Machine Learning
    ├── numpy/                      # Thao tác ma trận, mảng đa chiều với NumPy
    ├── matplotlib/                 # Trực quan hóa dữ liệu biểu đồ
    ├── scikit-learn/               # Huấn luyện mô hình cơ bản (Classification, Regression)
    ├── tokenizer/                  # Xử lý tokenization và từ điển văn bản
    └── exercises/                  # Bài tập lập trình thực hành & Jupyter Notebook demo
```

---

## 🛠️ Hướng dẫn cài đặt & Chạy dự án

### 1. Chuẩn bị môi trường Python
```bash
# Clone repository
git clone https://github.com/namnguyenit/python-data-hub.git
cd python-data-hub

# Tạo môi trường ảo (khuyến nghị)
python -m venv venv
# Kích hoạt trên Windows:
venv\Scripts\activate
# Kích hoạt trên Linux/macOS:
source venv/bin/activate
```

### 2. Cài đặt thư viện dependencies
```bash
pip install -r 1-premier-league-scraper/requirements.txt
pip install pandas numpy scikit-learn matplotlib jupyter seaborn
```

### 3. Chạy Premier League Scraper
```bash
cd 1-premier-league-scraper
cp .env.example .env
# Chỉnh sửa thông tin kết nối MySQL trong .env
python main.py
```

### 4. Chạy NLP Text Analytics Notebook
```bash
cd 2-nlp-text-analysis/notebooks
jupyter notebook Phan_tich_van_ban_NLP.ipynb
```

---

## 👨‍💻 Tác giả
- **Cao Đức Trung** ([@namnguyenit](https://github.com/namnguyenit))
- Dự án phục vụ mục đích học tập, nghiên cứu và thực hành Khoa học Dữ liệu.
