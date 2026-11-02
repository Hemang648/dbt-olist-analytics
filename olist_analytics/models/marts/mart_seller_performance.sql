with seller_orders as (
    -- one row per seller per order, so a multi-item order is not counted twice
    select
        i.seller_id,
        i.order_id,
        sum(i.price)           as revenue,
        o.delivery_days,
        o.is_delivered_late,
        o.review_score
    from {{ ref('fct_order_items') }} i
    inner join {{ ref('fct_orders') }} o
        on i.order_id = o.order_id
    where o.order_status = 'delivered'
    group by i.seller_id, i.order_id, o.delivery_days, o.is_delivered_late, o.review_score
),

sellers as (
    select seller_id, city, state, region
    from {{ ref('dim_sellers') }}
)

select
    seller_orders.seller_id,
    sellers.city,
    sellers.state,
    sellers.region,
    count(*)                                                         as orders,
    sum(seller_orders.revenue)                                       as revenue,
    round(avg(seller_orders.delivery_days), 1)                       as avg_delivery_days,
    round(avg(case when seller_orders.is_delivered_late then 1.0 else 0.0 end), 4) as late_rate,
    round(avg(seller_orders.review_score), 2)                        as avg_review_score
from seller_orders
left join sellers
    on seller_orders.seller_id = sellers.seller_id
group by 1, 2, 3, 4