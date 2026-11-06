import re
import logging
from typing import Dict, List, Set

# MySQL connector
try:
    import mysql.connector  # type: ignore
    HAS_MYSQL = True
except Exception:
    HAS_MYSQL = False

from config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DB,
    MYSQL_USER,
    MYSQL_PASSWORD,
)


def ten_cot_an_toan(name: str) -> str:
    s = re.sub(r"[^\w]+", "_", name.strip().lower())
    s = re.sub(r"_{2,}", "_", s).strip("_")
    if s == "":
        s = "col"
    return s


def ket_noi_mysql():
    if not HAS_MYSQL:
        logging.error("Chưa cài mysql-connector-python. Cài: pip install mysql-connector-python")
        return None
    if not (MYSQL_HOST and MYSQL_DB and MYSQL_USER and MYSQL_PASSWORD):
        logging.error("Thiếu cấu hình MySQL (MYSQL_HOST, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD).")
        return None
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=False,
    )


def cac_cot_trong_bang(conn, table: str) -> Set[str]:
    cols: Set[str] = set()
    cur = conn.cursor()
    try:
        cur.execute(f"SHOW COLUMNS FROM `{table}`")
        for row in cur.fetchall():
            cols.add(row[0])
    except Exception:
        pass
    finally:
        cur.close()
    return cols


def tao_bang_stats_if_chua_co(conn, table: str, columns: List[str]):
    cur = conn.cursor()
    sanitized = [ten_cot_an_toan(c) for c in columns]
    if "player_id" not in columns:
        sanitized = ["player_id"] + [c for c in sanitized if c != "player_id"]
    cur.execute(f"CREATE TABLE IF NOT EXISTS `{table}` (`player_id` VARCHAR(16) PRIMARY KEY)")
    conn.commit()
    existing = cac_cot_trong_bang(conn, table)
    for c in sanitized:
        if c not in existing:
            if c == "player_id":
                continue
            cur.execute(f"ALTER TABLE `{table}` ADD COLUMN `{c}` TEXT")
    conn.commit()
    cur.close()


def chen_hoac_capnhat_stats(conn, table: str, rows: List[Dict], columns: List[str]):
    if not rows:
        return
    cols = ["player_id"] + [c for c in columns if c != "player_id"]
    cols_sanitized = [ten_cot_an_toan(c) for c in cols]
    placeholders = ", ".join(["%s"] * len(cols))
    update_sql = ", ".join([f"`{ten_cot_an_toan(c)}`=VALUES(`{ten_cot_an_toan(c)}`)" for c in cols if c != "player_id"])
    sql = f"INSERT INTO `{table}` ({', '.join(f'`{c}`' for c in cols_sanitized)}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_sql}"
    cur = conn.cursor()
    batch = []
    for r in rows:
        values = []
        for c in cols:
            v = r.get(c, "N/a")
            if v is None or v == "":
                v = "N/a"
            values.append(v)
        batch.append(tuple(values))
    cur.executemany(sql, batch)
    conn.commit()
    cur.close()


def tao_bang_transfers_if_chua_co(conn, table: str):
    cur = conn.cursor()
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS `{table}` (
        `player_id` VARCHAR(16) PRIMARY KEY,
        `player_name` TEXT,
        `squad` TEXT,
        `value` TEXT,
        `currency` TEXT,
        `source_url` TEXT,
        `fetched_at` TEXT
    )
    """)
    conn.commit()
    cur.close()


def chen_hoac_capnhat_transfers(conn, table: str, rows: List[Dict]):
    if not rows:
        return
    sql = f"""
    INSERT INTO `{table}` (player_id, player_name, squad, value, currency, source_url, fetched_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        player_name=VALUES(player_name),
        squad=VALUES(squad),
        value=VALUES(value),
        currency=VALUES(currency),
        source_url=VALUES(source_url),
        fetched_at=VALUES(fetched_at)
    """
    cur = conn.cursor()
    data = [
        (
            r.get("player_id", "N/a") or "N/a",
            r.get("player_name", "N/a") or "N/a",
            r.get("squad", "N/a") or "N/a",
            r.get("value", "N/a") or "N/a",
            r.get("currency", "N/a") or "N/a",
            r.get("source_url", "N/a") or "N/a",
            r.get("fetched_at", "N/a") or "N/a",
        )
        for r in rows
    ]
    cur.executemany(sql, data)
    conn.commit()
    cur.close()
