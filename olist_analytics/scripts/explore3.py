import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(BASE_DIR / "dev.duckdb"), read_only=True)

print("products with no category")
print(con.sql("select count(*) as n from stg_products where category_name is null"))

print("categories with no English translation")
print(con.sql("""
    select p.category_name, count(*) as products
    from stg_products p
    left join stg_product_category_translation t on p.category_name = t.category_name
    where p.category_name is not null and t.category_name is null
    group by 1 order by 2 desc
"""))

print("translation table: duplicate keys?")
print(con.sql("""
    select count(*) as n, count(distinct category_name) as distinct_names
    from stg_product_category_translation
"""))

con.close()