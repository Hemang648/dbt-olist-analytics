import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(BASE_DIR / "dev.duckdb"), read_only=True)

print("row counts")
print(con.sql("""
    select 'dim_products' as model, count(*) as n from dim_products
    union all select 'dim_sellers', count(*) from dim_sellers
    union all select 'fct_order_items', count(*) from fct_order_items
    union all select 'mart_category_revenue', count(*) from mart_category_revenue
    union all select 'mart_delivery_performance_by_state', count(*) from mart_delivery_performance_by_state
    union all select 'mart_seller_performance', count(*) from mart_seller_performance
"""))

print("top 10 categories by revenue")
print(con.sql("""
    select revenue_rank, category, round(revenue) as revenue, revenue_share_pct
    from mart_category_revenue
    order by revenue_rank
    limit 10
"""))

print("slowest states (late rate)")
print(con.sql("""
    select state, region, delivered_orders, avg_delivery_days, late_rate, avg_review_score
    from mart_delivery_performance_by_state
    order by late_rate desc
    limit 10
"""))

print("late rate and review score by region")
print(con.sql("""
    select region,
           sum(delivered_orders) as orders,
           round(sum(late_orders) * 1.0 / sum(delivered_orders), 4) as late_rate
    from mart_delivery_performance_by_state
    group by 1 order by 3 desc
"""))

print("worst sellers with at least 30 orders")
print(con.sql("""
    select seller_id, state, orders, round(revenue) as revenue, late_rate, avg_review_score
    from mart_seller_performance
    where orders >= 30
    order by avg_review_score
    limit 10
"""))

con.close()