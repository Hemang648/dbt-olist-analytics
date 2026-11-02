with items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select
        order_id,
        customer_unique_id,
        customer_state,
        order_status,
        purchased_at
    from {{ ref('int_orders_enriched') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['items.order_id', 'items.order_item_id']) }} as order_item_key,
    items.order_id,
    items.order_item_id,
    items.product_id,
    items.seller_id,
    orders.customer_unique_id,
    orders.customer_state,
    orders.order_status,
    orders.purchased_at,
    items.shipping_limit_at,
    items.price,
    items.freight_value,
    items.price + items.freight_value as item_total
from items
inner join orders
    on items.order_id = orders.order_id