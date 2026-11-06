# EPL Player Analytics Scraper (2024-2025)

Thu thập thống kê cầu thủ Premier League 2024–2025 từ fbref.com và giá trị chuyển nhượng (xTV/Transfer Value) từ footballtransfers.com. Toàn bộ dữ liệu được ghi vào MySQL.

## Cấu trúc

- `config.py`: cấu hình URL, HTTP, MySQL, tên bảng, USE_SELENIUM.
- `http_utils.py`: session, fetch_url với retry/backoff, respectful_sleep.
- `fbref.py`: parse bảng Standard Stats cấp giải đấu, lọc Minutes > 90.
- `footballtransfers.py`: tìm và lấy giá trị cầu thủ; Selenium fallback.
- `mysql_db.py`: kết nối MySQL, tạo bảng nếu thiếu, upsert dữ liệu.
- `main.py`: pipeline điều phối.

## Chuẩn bị môi trường (Windows cmd)

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Cấu hình bằng file .env

Bạn có thể tạo file `.env` (đã có sẵn mẫu `.env.example`) và sửa thông tin:

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=your_db
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
USE_SELENIUM=0
TARGET_MINUTES=90
REQUEST_TIMEOUT=30
MAX_RETRIES=5
BACKOFF_BASE=1.6
FBREF_LEAGUE_PLAYERS_URL=https://fbref.com/en/comps/9/2024-2025/players/2024-2025-Premier-League-Players
```

Chương trình sẽ tự động đọc `.env` (nhờ python-dotenv).

Ghi chú:
- TARGET_MINUTES = 0 để lấy tất cả cầu thủ (không lọc theo phút thi đấu).
- Các thông số HTTP giúp điều chỉnh retry/backoff khi bị rate-limit.

## Chạy

```bat
python main.py
```

## Gợi ý giảm CAPTCHA / rate-limit
- Thêm delay ngẫu nhiên và exponential backoff (đã tích hợp).
- Xoay User-Agent, tránh song song nhiều luồng, tôn trọng robots.txt.
- Khi bị chặn, bật Selenium undetected-chromedriver, giảm tốc độ crawl.
