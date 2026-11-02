-- item prices in fct_order_items must add up to items_value in fct_orders
select
    o.order_id,
    o.items_value,
    i.items_sum
from {{ ref('fct_orders') }} o
inner join (
    select order_id, sum(price) as items_sum
    from {{ ref('fct_order_items') }}
    group by order_id
) i
    on o.order_id = i.order_id
where abs(o.items_value - i.items_sum) > 0.01