import re
import urllib.parse
from typing import Optional, Tuple

from bs4 import BeautifulSoup

from http_utils import tao_session, tai_url, tam_dung
from config import USE_SELENIUM

# Optional selenium fallback
try:
    if USE_SELENIUM:
        import undetected_chromedriver as uc  # type: ignore
        from selenium.webdriver.common.by import By  # type: ignore
        from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
        from selenium.webdriver.support import expected_conditions as EC  # type: ignore
        HAS_SELENIUM = True
    else:
        HAS_SELENIUM = False
except Exception:
    HAS_SELENIUM = False


def tao_session_ft():
    s = tao_session()
    s.headers.update({"Referer": "https://www.footballtransfers.com/"})
    return s


def tim_cau_thu_ft(session, ten: str, doi: Optional[str] = None) -> Optional[str]:
    q = urllib.parse.quote(ten)
    url = f"https://www.footballtransfers.com/en/search?keyword={q}"
    html = tai_url(session, url)
    tam_dung(1.0)
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")
    candidates = []
    for a in soup.select("a[href*='/en/players/']"):
        href = a.get("href")
        if not href:
            continue
        name_txt = a.get_text(strip=True)
        context = a.parent.get_text(" ", strip=True) if a.parent else name_txt
        score = 0
        if name_txt.lower() == ten.lower():
            score += 5
        # slug match boost
        slug = href.lower()
        for token in re.split(r"\s+", ten.lower()):
            if token and token in slug:
                score += 1
        # club/squad match boost
        if doi:
            doi_l = doi.lower()
            if doi_l in context.lower():
                score += 4
        candidates.append((score, href))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        best = candidates[0][1]
        return urllib.parse.urljoin("https://www.footballtransfers.com", best)
    return None


def phan_tich_gia_tri_ft(html: str) -> Tuple[str, str]:
    soup = BeautifulSoup(html, "lxml")
    candidates = []
    for el in soup.find_all(text=re.compile(r"(xTV|Transfer Value|Current Value)", re.I)):
        box = el.parent
        for _ in range(3):
            if box is None:
                break
            nums = re.findall(r"([€£$]\s?\d[\d\.,]*\s?[mk]?)", box.get_text(" ", strip=True), flags=re.I)
            if nums:
                candidates.extend(nums)
                break
            box = box.parent
    if not candidates:
        text = soup.get_text(" ", strip=True)
        candidates = re.findall(r"([€£$]\s?\d[\d\.,]*\s?[mk]?)", text, flags=re.I)
    if candidates:
        val = candidates[0]
        cur = "EUR" if "€" in val else "GBP" if "£" in val else "USD" if "$" in val else "N/a"
        return val, cur
    return "N/a", "N/a"


def selenium_driver():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    return driver


_SELENIUM_DRIVER = None


def selenium_tim_cau_thu(ten: str) -> Optional[str]:
    global _SELENIUM_DRIVER
    if not HAS_SELENIUM:
        return None
    if _SELENIUM_DRIVER is None:
        _SELENIUM_DRIVER = selenium_driver()
    q = urllib.parse.quote(ten)
    url = f"https://www.footballtransfers.com/en/search?keyword={q}"
    _SELENIUM_DRIVER.get(url)
    try:
        WebDriverWait(_SELENIUM_DRIVER, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/en/players/']"))
        )
    except Exception:
        return None
    links = _SELENIUM_DRIVER.find_elements(By.CSS_SELECTOR, "a[href*='/en/players/']")
    for a in links:
        try:
            txt = a.text.strip()
            href = a.get_attribute("href")
            if href and "/en/players/" in href:
                if txt.lower() == ten.lower():
                    return href
        except Exception:
            continue
    if links:
        return links[0].get_attribute("href")
    return None


def selenium_lay_html(url: str) -> Optional[str]:
    global _SELENIUM_DRIVER
    if not HAS_SELENIUM:
        return None
    if _SELENIUM_DRIVER is None:
        _SELENIUM_DRIVER = selenium_driver()
    _SELENIUM_DRIVER.get(url)
    try:
        WebDriverWait(_SELENIUM_DRIVER, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return _SELENIUM_DRIVER.page_source
    except Exception:
        return None


def lay_gia_tri_cau_thu(ten: str, doi: Optional[str] = None) -> Tuple[str, str, str]:
    session = tao_session_ft()
    url = tim_cau_thu_ft(session, ten, doi)
    if not url and HAS_SELENIUM:
        # Selenium: vẫn tìm theo tên nếu không có URL
        url = selenium_tim_cau_thu(ten)
    if not url:
        return "N/a", "N/a", "N/a"

    html = tai_url(session, url)
    tam_dung(1.0)
    if (not html) and HAS_SELENIUM:
        html = selenium_lay_html(url)

    if not html:
        return "N/a", "N/a", url

    value, currency = phan_tich_gia_tri_ft(html)
    return value, currency, url


def selenium_cleanup():
    global _SELENIUM_DRIVER
    try:
        if _SELENIUM_DRIVER:
            _SELENIUM_DRIVER.quit()
    except Exception:
        pass
