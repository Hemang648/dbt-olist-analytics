import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(BASE_DIR / "dev.duckdb"))

seller_id = con.execute("select seller_id from raw.sellers order by seller_id limit 1").fetchone()[0]
con.execute("update raw.sellers set seller_city = ? where seller_id = ?", ["demo city", seller_id])
print(f"Changed city for seller {seller_id}")
con.close()