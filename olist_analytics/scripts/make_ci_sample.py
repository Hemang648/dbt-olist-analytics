"""Build a small, deterministic sample of the Olist data for CI.

Reads the full raw tables from dev.duckdb (run load_raw.py first) and writes
sample CSVs with the original file names into olist_analytics/ci_data/.

The sample is referentially closed: every sampled order brings along its
customer, items, payments and reviews, and every item brings its product and
seller. That keeps relationship tests meaningful on the small dataset.

Usage:
    python scripts/make_ci_sample.py          # 3000 orders
    python scripts/make_ci_sample.py 5000     # custom number of orders
"""
import sys
from pathlib import Path

import duckdb

N_ORDERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
GEO_ROWS_PER_ZIP = 5

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "ci_data"
OUT_DIR.mkdir(exist_ok=True)

con = duckdb.connect(str(BASE_DIR / "dev.duckdb"), read_only=True)

# Ordering by a hash makes the "random" sample repeatable.
ORDERS = f"(select * from raw.orders order by md5(order_id) limit {N_ORDERS})"
ORDER_IDS = f"(select order_id from {ORDERS})"
CUSTOMER_IDS = f"(select customer_id from {ORDERS})"
ITEMS = f"(select * from raw.order_items where order_id in {ORDER_IDS})"
PRODUCT_IDS = f"(select product_id from {ITEMS})"
SELLER_IDS = f"(select seller_id from {ITEMS})"
ZIPS = f"""(
    select customer_zip_code_prefix from raw.customers where customer_id in {CUSTOMER_IDS}
    union
    select seller_zip_code_prefix from raw.sellers where seller_id in {SELLER_IDS}
)"""

queries = {
    "olist_orders_dataset.csv": f"select * from {ORDERS}",
    "olist_customers_dataset.csv": f"select * from raw.customers where customer_id in {CUSTOMER_IDS}",
    "olist_order_items_dataset.csv": f"select * from {ITEMS}",
    "olist_order_payments_dataset.csv": f"select * from raw.order_payments where order_id in {ORDER_IDS}",
    "olist_order_reviews_dataset.csv": f"select * from raw.order_reviews where order_id in {ORDER_IDS}",
    "olist_products_dataset.csv": f"select * from raw.products where product_id in {PRODUCT_IDS}",
    "olist_sellers_dataset.csv": f"select * from raw.sellers where seller_id in {SELLER_IDS}",
    # Geolocation has about 52 rows per zip, so keep a few per zip to stay small.
    "olist_geolocation_dataset.csv": f"""
        select geolocation_zip_code_prefix, geolocation_lat, geolocation_lng,
               geolocation_city, geolocation_state
        from (
            select *,
                   row_number() over (
                       partition by geolocation_zip_code_prefix
                       order by geolocation_lat, geolocation_lng
                   ) as rn
            from raw.geolocation
            where geolocation_zip_code_prefix in {ZIPS}
        )
        where rn <= {GEO_ROWS_PER_ZIP}
    """,
    "product_category_name_translation.csv": "select * from raw.product_category_translation",
}

for filename, query in queries.items():
    out = (OUT_DIR / filename).as_posix()
    con.execute(f"COPY ({query}) TO '{out}' (HEADER, DELIMITER ',')")
    n = con.execute(f"select count(*) from ({query})").fetchone()[0]
    print(f"{filename}: {n:,} rows")


def csv(name):
    return f"read_csv('{(OUT_DIR / name).as_posix()}', header = true, all_varchar = true)"


# Referential integrity checks on the files we just wrote.
checks = {
    "orders without a customer": f"""
        select count(*) from {csv('olist_orders_dataset.csv')} o
        left join {csv('olist_customers_dataset.csv')} c using (customer_id)
        where c.customer_id is null""",
    "items without a product": f"""
        select count(*) from {csv('olist_order_items_dataset.csv')} i
        left join {csv('olist_products_dataset.csv')} p using (product_id)
        where p.product_id is null""",
    "items without a seller": f"""
        select count(*) from {csv('olist_order_items_dataset.csv')} i
        left join {csv('olist_sellers_dataset.csv')} s using (seller_id)
        where s.seller_id is null""",
}

failed = False
for label, sql in checks.items():
    n = con.execute(sql).fetchone()[0]
    print(f"check - {label}: {n}")
    failed = failed or n != 0

con.close()

if failed:
    sys.exit("Sample is not referentially consistent. Check the output above.")
print(f"\nSample written to {OUT_DIR}")