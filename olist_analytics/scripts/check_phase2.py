import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(BASE_DIR / "dev.duckdb"), read_only=True)

print("row counts")
print(con.sql("""
    select 'stg_orders' as model, count(*) as n from stg_orders
    union all select 'int_orders_enriched', count(*) from int_orders_enriched
    union all select 'fct_orders', count(*) from fct_orders
    union all select 'dim_customers', count(*) from dim_customers
    union all select 'int_geolocation_by_zip', count(*) from int_geolocation_by_zip
    union all select 'int_order_reviews_deduped', count(*) from int_order_reviews_deduped
"""))

print("repeat customers")
print(con.sql("""
    select is_repeat_customer, count(*) as customers
    from dim_customers
    group by 1
"""))

print("late delivery vs review score (delivered orders)")
print(con.sql("""
    select is_delivered_late, count(*) as orders, round(avg(review_score), 2) as avg_review
    from fct_orders
    where order_status = 'delivered'
    group by 1
    order by 1
"""))

con.close()