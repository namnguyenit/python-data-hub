import os

# Nạp biến môi trường từ file .env (nếu có)
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # Nếu chưa cài python-dotenv, vẫn chạy bình thường với biến môi trường sẵn có
    pass

# FBref
FBREF_LEAGUE_PLAYERS_URL = os.getenv(
    "FBREF_LEAGUE_PLAYERS_URL",
    "https://fbref.com/en/comps/9/2024-2025/players/2024-2025-Premier-League-Players",
)
# League Stats page (yêu cầu mới): vào trang tổng trước rồi đi từng đội
FBREF_LEAGUE_STATS_URL = os.getenv(
    "FBREF_LEAGUE_STATS_URL",
    "https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats",
)
# Số phút tối thiểu để lọc cầu thủ. Đặt 0 để lấy tất cả.
try:
    TARGET_MINUTES = int(os.getenv("TARGET_MINUTES", "90"))
except Exception:
    TARGET_MINUTES = 90

# HTTP
try:
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
except Exception:
    REQUEST_TIMEOUT = 30
try:
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))
except Exception:
    MAX_RETRIES = 5
try:
    BACKOFF_BASE = float(os.getenv("BACKOFF_BASE", "1.6"))
except Exception:
    BACKOFF_BASE = 1.6

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/127.0.0.0 Chrome/127.0.0.0 Safari/537.36",
]
HEADERS_BASE = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Connection": "keep-alive",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "no-cache",
}

# MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DB = os.getenv("MYSQL_DB", "")
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

MYSQL_TABLE_STATS = "epl_player_stats_2024_2025"
MYSQL_TABLE_TRANSFERS = "player_transfers_2024_2025"

# Optional Selenium
USE_SELENIUM = os.getenv("USE_SELENIUM", "0") == "1"
