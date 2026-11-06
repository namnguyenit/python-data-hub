import random
import time
import logging
from typing import Optional

import requests

from config import HEADERS_BASE, USER_AGENTS, REQUEST_TIMEOUT, MAX_RETRIES, BACKOFF_BASE


def _random_ua() -> str:
    if USER_AGENTS:
        return random.choice(USER_AGENTS)
    return "Mozilla/5.0"


def tao_session() -> requests.Session:
    """Tạo session đơn giản với headers cơ bản."""
    s = requests.Session()
    # Cho phép dùng proxy từ biến môi trường (HTTP(S)_PROXY, NO_PROXY, ...)
    s.trust_env = True
    s.headers.update(HEADERS_BASE)
    s.headers.update({
        "User-Agent": _random_ua(),
        "Accept-Encoding": "gzip, deflate, br, zstd",
    })
    return s


def tam_dung(giay: float = 1.0) -> None:
    """Tạm dừng vài giây cho lịch sự."""
    time.sleep(giay)


def tai_url(session: requests.Session, url: str) -> Optional[str]:
    """Tải nội dung HTML của URL với retry và backoff. Lỗi thì trả về None."""
    last_exc: Optional[Exception] = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Đổi UA và đặt Referer theo domain mỗi lần thử
            session.headers.update({"User-Agent": _random_ua()})
            low = url.lower()
            if "fbref.com" in low:
                session.headers.update({"Referer": "https://fbref.com/en/"})
            elif "footballtransfers.com" in low:
                session.headers.update({"Referer": "https://www.footballtransfers.com/"})

            resp = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            code = resp.status_code

            if code in (403, 429):
                # Bị chặn/giới hạn — backoff mạnh hơn, thử lại
                delay = (BACKOFF_BASE ** attempt) + random.uniform(1.0, 2.5)
                logging.warning("HTTP %s khi tải %s (attempt %d/%d). Backoff %.2fs",
                                code, url, attempt, MAX_RETRIES, delay)
                time.sleep(delay)
                continue

            if code >= 500:
                raise requests.HTTPError(f"{code}")

            resp.raise_for_status()
            return resp.text
        except Exception as e:
            last_exc = e
            # exponential backoff + jitter
            delay = (BACKOFF_BASE ** (attempt - 1)) + random.uniform(0, 0.5)
            logging.warning("Lỗi khi tải %s (attempt %d/%d): %s. Chờ %.2fs",
                            url, attempt, MAX_RETRIES, str(e), delay)
            time.sleep(delay)
            continue
    logging.error("Tải thất bại sau %d lần: %s; lỗi cuối: %s", MAX_RETRIES, url, repr(last_exc))
    return None
