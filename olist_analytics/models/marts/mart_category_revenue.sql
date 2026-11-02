with items as (
    select * from {{ ref('fct_order_items') }}
    where order_status = 'delivered'
),

products as (
    select product_id, category_name_english
    from {{ ref('dim_products') }}
)

select
    coalesce(products.category_name_english, 'unknown')            as category,
    count(distinct items.order_id)                                 as orders,
    count(*)                                                       as items_sold,
    sum(items.price)                                               as revenue,
    sum(items.freight_value)                                       as freight,
    round(avg(items.price), 2)                                     as avg_item_price,
    round(sum(items.price) * 100.0 / sum(sum(items.price)) over (), 2) as revenue_share_pct,
    rank() over (order by sum(items.price) desc)                   as revenue_rank
from items
left join products
    on items.product_id = products.product_id
group by 1