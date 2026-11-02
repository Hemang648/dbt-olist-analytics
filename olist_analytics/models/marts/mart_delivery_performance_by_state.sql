select
    customer_state                                                   as state,
    {{ state_to_region('customer_state') }}                          as region,
    count(*)                                                         as delivered_orders,
    round(avg(delivery_days), 1)                                     as avg_delivery_days,
    sum(case when is_delivered_late then 1 else 0 end)               as late_orders,
    round(avg(case when is_delivered_late then 1.0 else 0.0 end), 4) as late_rate,
    round(avg(review_score), 2)                                      as avg_review_score
from {{ ref('fct_orders') }}
where order_status = 'delivered'
  and delivered_at is not null
group by 1, 2