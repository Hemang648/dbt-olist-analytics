import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(BASE_DIR / "dev.duckdb"))

print(con.sql("select count(*) as rows_before from fct_orders"))
con.execute("delete from fct_orders where purchased_at >= '2018-08-01'")
print(con.sql("select count(*) as rows_after_delete, max(purchased_at) as latest from fct_orders"))
con.close()