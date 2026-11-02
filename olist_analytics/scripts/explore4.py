import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(BASE_DIR / "dev.duckdb"), read_only=True)

print("mismatch direction")
print(con.sql("""
    select
        case when total_payment_value > items_value + freight_value
             then 'paid more than items + freight'
             else 'paid less than items + freight' end as direction,
        count(*) as orders
    from fct_orders
    where order_status = 'delivered'
      and abs(total_payment_value - (items_value + freight_value)) > 1
    group by 1
"""))

print("mismatch by installments")
print(con.sql("""
    select coalesce(max_installments > 1, false) as paid_in_installments, count(*) as orders
    from fct_orders
    where order_status = 'delivered'
      and abs(total_payment_value - (items_value + freight_value)) > 1
    group by 1
"""))

con.close()