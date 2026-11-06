import logging
from datetime import datetime

from config import MYSQL_TABLE_STATS, MYSQL_TABLE_TRANSFERS
from fbref import lay_ds_cau_thu_fbref, selenium_cleanup_fbref
from footballtransfers import lay_gia_tri_cau_thu, selenium_cleanup
from http_utils import tam_dung
from mysql_db import (
	ket_noi_mysql,
	tao_bang_stats_if_chua_co,
	chen_hoac_capnhat_stats,
	tao_bang_transfers_if_chua_co,
	chen_hoac_capnhat_transfers,
)


def chuong_trinh_chinh():
	logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

	logging.info("Đang lấy danh sách cầu thủ từ fbref...")
	ds_cau_thu, ds_cot = lay_ds_cau_thu_fbref()
	logging.info("Tìm thấy %d cầu thủ.", len(ds_cau_thu))

	conn = ket_noi_mysql()
	if not conn:
		return

	# Ghi stats vào MySQL
	tao_bang_stats_if_chua_co(conn, MYSQL_TABLE_STATS, ds_cot)
	chen_hoac_capnhat_stats(conn, MYSQL_TABLE_STATS, ds_cau_thu, ds_cot)
	logging.info("Đã ghi %d dòng vào %s", len(ds_cau_thu), MYSQL_TABLE_STATS)

	# Lấy giá và ghi vào MySQL
	tao_bang_transfers_if_chua_co(conn, MYSQL_TABLE_TRANSFERS)
	hang_chuyen_nhuong = []
	for i, p in enumerate(ds_cau_thu, 1):
		ten = p.get("player", "N/a")
		pid = p.get("player_id", f"noid_{i}")
		doi = p.get("squad", "N/a")

		gia, tien_te, url = lay_gia_tri_cau_thu(ten, doi)
		now = datetime.utcnow().isoformat(timespec="seconds") + "Z"
		hang_chuyen_nhuong.append({
			"player_id": pid,
			"player_name": ten,
			"squad": doi,
			"value": gia or "N/a",
			"currency": tien_te or "N/a",
			"source_url": url or "N/a",
			"fetched_at": now,
		})
		logging.info("(%d/%d) %s -> %s %s", i, len(ds_cau_thu), ten, tien_te, gia)
		tam_dung(1.0)

	chen_hoac_capnhat_transfers(conn, MYSQL_TABLE_TRANSFERS, hang_chuyen_nhuong)
	logging.info("Đã ghi %d dòng vào %s", len(hang_chuyen_nhuong), MYSQL_TABLE_TRANSFERS)

	try:
		selenium_cleanup()
		selenium_cleanup_fbref()
	finally:
		conn.close()


if __name__ == "__main__":
	chuong_trinh_chinh()
