import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(BASE_DIR / "dev.duckdb"), read_only=True)

print("status of orders with no items")
print(con.sql("""
    select o.order_status, count(*) as n
    from raw.orders o
    left join raw.order_items i using (order_id)
    where i.order_id is null
    group by 1 order by 2 desc
"""))

print("duplicate review_ids: same order or different orders?")
print(con.sql("""
    select count(*) as duplicated_review_ids,
           sum(case when orders_per_review = 1 then 1 else 0 end) as same_order,
           sum(case when orders_per_review > 1 then 1 else 0 end) as different_orders
    from (
        select review_id, count(distinct order_id) as orders_per_review
        from raw.order_reviews
        group by 1
        having count(*) > 1
    )
"""))

print("orders with more than one review")
print(con.sql("""
    select count(*) as orders_with_multiple_reviews
    from (select order_id from raw.order_reviews group by 1 having count(*) > 1)
"""))

print("delivered orders with no delivery date")
print(con.sql("""
    select count(*) as delivered_without_date
    from raw.orders
    where order_status = 'delivered' and order_delivered_customer_date is null
"""))

print("orders with more than one payment row")
print(con.sql("""
    select count(*) as orders_with_multiple_payments
    from (select order_id from raw.order_payments group by 1 having count(*) > 1)
"""))

con.close() 