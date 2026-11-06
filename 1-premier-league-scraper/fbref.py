import re
import urllib.parse
import logging
import random
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, Comment

from http_utils import tao_session, tai_url, tam_dung
from config import FBREF_LEAGUE_PLAYERS_URL, FBREF_LEAGUE_STATS_URL, TARGET_MINUTES, USE_SELENIUM, USER_AGENTS

# Optional Selenium fallback for fbref
try:
    if USE_SELENIUM:
        import undetected_chromedriver as uc  # type: ignore
        from selenium.webdriver.common.by import By  # type: ignore
        from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
        from selenium.webdriver.support import expected_conditions as EC  # type: ignore
        HAS_SELENIUM_FBREF = True
    else:
        HAS_SELENIUM_FBREF = False
except Exception:
    HAS_SELENIUM_FBREF = False

_FBREF_DRIVER = None

def _selenium_fbref_driver():
    global _FBREF_DRIVER
    if _FBREF_DRIVER is None:
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        try:
            ua = random.choice(USER_AGENTS) if USER_AGENTS else "Mozilla/5.0"
            options.add_argument(f"--user-agent={ua}")
        except Exception:
            pass
        _FBREF_DRIVER = uc.Chrome(options=options)
    return _FBREF_DRIVER

def selenium_lay_html_fbref(url: str) -> Optional[str]:
    if not HAS_SELENIUM_FBREF:
        return None
    try:
        driver = _selenium_fbref_driver()
    except Exception as e:
        logging.warning("Khởi tạo Selenium fbref lỗi: %s", e)
        return None
    try:
        # Prewarm domain để set cookies/consent
        driver.get("https://fbref.com/en/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # Cố gắng bấm đồng ý cookie nếu có
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for b in buttons:
                try:
                    txt = (b.text or "").strip().lower()
                    if any(k in txt for k in ["accept", "agree", "i agree", "allow all"]):
                        if b.is_displayed():
                            b.click()
                            break
                except Exception:
                    continue
        except Exception:
            pass
        tam_dung(1.0)
        # Tải trang đích
        driver.get(url)
        WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        return driver.page_source
    except Exception as e:
        logging.warning("Selenium tải fbref thất bại: %s", e)
        return None

def selenium_cleanup_fbref():
    global _FBREF_DRIVER
    try:
        if _FBREF_DRIVER:
            _FBREF_DRIVER.quit()
    except Exception:
        pass

def tim_bang_trong_comment(soup: BeautifulSoup, table_id: str):
    t = soup.find("table", id=table_id)
    if t:
        return t
    for c in soup.find_all(string=lambda text: isinstance(text, Comment)):
        try:
            csoup = BeautifulSoup(c, "lxml")
            t2 = csoup.find("table", id=table_id)
            if t2:
                return t2
        except Exception:
            continue
    return None


def lay_text_o(tag) -> str:
    txt = tag.get_text(separator=" ", strip=True)
    return txt if txt != "" else "N/a"


def lay_ma_cau_thu_tu_href(href: str) -> Optional[str]:
    m = re.search(r"/players/([a-f0-9]{8})/", href)
    if m:
        return m.group(1)
    m = re.search(r"/players/([a-f0-9]{8})(?:/|$)", href)
    return m.group(1) if m else None


def chuyen_so(s: Optional[str]) -> Optional[int]:
    if not s or s == "N/a":
        return None
    try:
        import re as _re
        return int(_re.sub(r"[^\d]", "", s))
    except Exception:
        return None


def phan_tich_fbref_players(html: str) -> Tuple[List[Dict], List[str]]:
    soup = BeautifulSoup(html, "lxml")
    table = tim_bang_trong_comment(soup, "stats_standard")
    if table is None:
        candidates = soup.select("table[id*='standard']")
        table = candidates[0] if candidates else None
    if table is None:
        raise RuntimeError("Không tìm thấy bảng 'Standard Stats' trên fbref.")

    header_ths = table.find("thead").find_all("th")
    data_stats = []
    for th in header_ths:
        ds = th.get("data-stat")
        if ds and ds not in data_stats:
            data_stats.append(ds)

    rows = []
    tbody = table.find("tbody")
    for tr in tbody.find_all("tr"):
        if "class" in tr.attrs and "thead" in tr.get("class", []):
            continue
        row = {}
        th = tr.find("th")
        if th:
            ds = th.get("data-stat")
            val = lay_text_o(th)
            if ds:
                row[ds] = val
            a = th.find("a", href=True)
            if a and a["href"]:
                row["player_url"] = urllib.parse.urljoin("https://fbref.com", a["href"])
                pid = lay_ma_cau_thu_tu_href(a["href"])
                if pid:
                    row["player_id"] = pid

        for td in tr.find_all("td"):
            ds = td.get("data-stat")
            if not ds:
                continue
            row[ds] = lay_text_o(td)
            if ds == "squad":
                a = td.find("a", href=True)
                if a and a["href"]:
                    row["squad_url"] = urllib.parse.urljoin("https://fbref.com", a["href"])

        if not row.get("player"):
            continue
        rows.append(row)

    filtered = []
    for r in rows:
        mins = chuyen_so(r.get("minutes"))
        if mins is not None and mins > TARGET_MINUTES:
            filtered.append(r)

    essential = ["player_id", "player", "squad", "position", "age", "birth_year", "minutes"]
    for k in essential:
        if k not in data_stats:
            data_stats.append(k)

    seen_keys = set()
    for r in filtered:
        for k in r.keys():
            seen_keys.add(k)
    ordered_cols = [c for c in data_stats if c in seen_keys] + [c for c in sorted(seen_keys) if c not in data_stats]
    return filtered, ordered_cols

# Helpers for league->teams crawl
def _trich_xuat_team_urls(html_str: str) -> List[str]:
    soup = BeautifulSoup(html_str, "lxml")
    teams: List[str] = []
    seen = set()
    for a in soup.select("a[href^='/en/squads/']"):
        href = a.get("href") or ""
        if re.search(r"^/en/squads/[a-f0-9]{8}/2024-2025/.+-Stats$", href):
            full = urllib.parse.urljoin("https://fbref.com", href)
            if full not in seen:
                seen.add(full)
                teams.append(full)
    return teams

def _extract_team_name(soup: BeautifulSoup) -> str:
    try:
        h1 = soup.select_one("h1")
        if h1:
            txt = h1.get_text(" ", strip=True)
            return txt.replace(" Stats", "").strip()
    except Exception:
        pass
    return "N/a"

def _parse_team_player_tables(html_str: str, team_name: str) -> Tuple[List[Dict], List[str]]:
    soup = BeautifulSoup(html_str, "lxml")
    prefixes = [
        "stats_standard",
        "stats_playing_time",
        "stats_shooting",
        "stats_passing",
        "stats_passing_types",
        "stats_gca",
        "stats_defense",
        "stats_possession",
        "stats_misc",
        "stats_keeper",
        "stats_keeper_adv",
    ]
    per_player: Dict[str, Dict] = {}
    all_cols: List[str] = []

    def _add_col(c: str):
        if c not in all_cols:
            all_cols.append(c)

    for table_id in prefixes:
        t = tim_bang_trong_comment(soup, table_id)
        if t is None:
            continue
        prefix = table_id.replace("stats_", "")
        tbody = t.find("tbody")
        if not tbody:
            continue
        for tr in tbody.find_all("tr"):
            if "class" in tr.attrs and "thead" in tr.get("class", []):
                continue
            th = tr.find("th")
            if not th:
                continue
            a = th.find("a", href=True)
            pid = None
            if a and a.get("href"):
                pid = lay_ma_cau_thu_tu_href(a["href"])
            name = lay_text_o(th)
            if not pid and name and name != "N/a":
                pid = name.lower().strip().replace(" ", "_")
            if not pid:
                continue
            row = per_player.get(pid, {"player_id": pid, "player": name, "squad": team_name})
            if a and a.get("href") and "player_url" not in row:
                row["player_url"] = urllib.parse.urljoin("https://fbref.com", a["href"])

            # th cell
            ds_th = th.get("data-stat")
            if ds_th:
                key = f"{prefix}_{ds_th}"
                if key not in row:
                    row[key] = lay_text_o(th)
                    _add_col(key)

            # td cells
            for td in tr.find_all("td"):
                ds = td.get("data-stat")
                if not ds:
                    continue
                key = f"{prefix}_{ds}"
                row[key] = lay_text_o(td)
                _add_col(key)

            per_player[pid] = row

    rows = list(per_player.values())
    cols = list(all_cols)
    for base in ["player_id", "player", "squad"]:
        if base not in cols:
            if base == "player_id":
                cols.insert(0, base)
            else:
                cols.append(base)
    return rows, cols

def lay_ds_cau_thu_fbref() -> Tuple[list, list]:
    """
    Crawl theo yêu cầu:
    - Vào trang league stats tổng
    - Lấy link từng đội
    - Vào từng đội, hợp bảng stats_* để lấy full chỉ số cầu thủ
    - Lọc phút > TARGET_MINUTES
    """
    session = tao_session()

    # Ưu tiên Selenium trước để tránh 403/Cloudflare
    html = selenium_lay_html_fbref(FBREF_LEAGUE_STATS_URL) if HAS_SELENIUM_FBREF else None
    if not html:
        html = tai_url(session, FBREF_LEAGUE_STATS_URL)
    if not html:
        raise RuntimeError("Không tải được trang fbref (league stats).")
    tam_dung(2.0)

    team_urls = _trich_xuat_team_urls(html)
    if not team_urls:
        raise RuntimeError("Không tìm thấy danh sách đội ở trang league stats.")

    merged: Dict[str, Dict] = {}
    col_order: List[str] = ["player_id", "player", "squad"]
    col_seen = set(col_order)

    for tu in team_urls:
        # Ưu tiên Selenium trước để giảm 403, sau đó mới dùng requests
        thtml = selenium_lay_html_fbref(tu) if HAS_SELENIUM_FBREF else None
        if not thtml:
            thtml = tai_url(session, tu)
        if not thtml:
            continue
        tsoup = BeautifulSoup(thtml, "lxml")
        team_name = _extract_team_name(tsoup)
        rows, cols = _parse_team_player_tables(thtml, team_name)
        tam_dung(1.5)

        # hợp nhất cột
        for c in cols:
            if c not in col_seen:
                col_seen.add(c)
                col_order.append(c)

        # hợp nhất dữ liệu theo player_id
        for r in rows:
            pid = r.get("player_id")
            if not pid:
                continue
            existed = merged.get(pid, {})
            existed.update(r)
            merged[pid] = existed

    # Lọc phút > TARGET_MINUTES (ưu tiên standard_minutes, rồi *_minutes, rồi minutes)
    def _get_minutes(d: Dict) -> Optional[int]:
        if "standard_minutes" in d:
            return chuyen_so(d.get("standard_minutes"))
        for k in list(d.keys()):
            if k.endswith("_minutes"):
                m = chuyen_so(d.get(k))
                if m is not None:
                    return m
        return chuyen_so(d.get("minutes"))

    filtered = []
    for v in merged.values():
        mins = _get_minutes(v)
        if mins is not None and mins > TARGET_MINUTES:
            filtered.append(v)

    # Chỉ giữ cột thực sự xuất hiện
    present = set()
    for r in filtered:
        present.update(r.keys())
    ordered_cols = [c for c in col_order if c in present]

    return filtered, ordered_cols
