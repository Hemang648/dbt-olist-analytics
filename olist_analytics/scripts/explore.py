import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(BASE_DIR / "dev.duckdb"), read_only=True)

print("customer_id vs customer_unique_id")
print(con.sql("""
    select count(distinct customer_id) as customer_ids,
           count(distinct customer_unique_id) as unique_people
    from raw.customers
"""))

print("duplicate review_ids")
print(con.sql("""
    select count(*) as total_rows, count(distinct review_id) as distinct_review_ids
    from raw.order_reviews
"""))

print("geolocation rows per zip prefix")
print(con.sql("""
    select count(*) as rows, count(distinct geolocation_zip_code_prefix) as zips
    from raw.geolocation
"""))

print("order statuses")
print(con.sql("""
    select order_status, count(*) as n
    from raw.orders group by 1 order by 2 desc
"""))

print("orders with no items")
print(con.sql("""
    select count(*) as orders_without_items
    from raw.orders o
    left join raw.order_items i using (order_id)
    where i.order_id is null
"""))

con.close()