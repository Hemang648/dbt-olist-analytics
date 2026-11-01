
import sys
import duckdb
from pathlib import Path

# Project root directory (one level above scripts)
BASE_DIR = Path(__file__).resolve().parent.parent

# Database path
db = sys.argv[1] if len(sys.argv) > 1 else str(BASE_DIR / "dev.duckdb")

# Raw CSV directory
RAW_DIR = BASE_DIR / "data" / "raw"

# Table name -> CSV file
files = {
    'customers': 'olist_customers_dataset.csv',
    'geolocation': 'olist_geolocation_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
    'order_payments': 'olist_order_payments_dataset.csv',
    'order_reviews': 'olist_order_reviews_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'product_category_translation': 'product_category_name_translation.csv',
}

con = duckdb.connect(db)

con.sql("CREATE SCHEMA IF NOT EXISTS raw")

for table, csv in files.items():

    csv_path = RAW_DIR / csv

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    con.execute("""
        CREATE OR REPLACE TABLE raw.{} AS
        SELECT *
        FROM read_csv(?, header = true, all_varchar = true)
    """.format(table), [str(csv_path)])

    n = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]

    print(f"raw.{table}: {n:,} rows")

con.close()

print("\nAll raw tables loaded successfully!")
