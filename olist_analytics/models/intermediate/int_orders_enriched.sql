with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

items as (
    select * from {{ ref('int_order_items_agg') }}
),

payments as (
    select * from {{ ref('int_order_payments_pivoted') }}
),

reviews as (
    select * from {{ ref('int_order_reviews_deduped') }}
)

select
    orders.order_id,
    orders.customer_id,
    customers.customer_unique_id,
    customers.city             as customer_city,
    customers.state            as customer_state,
    customers.zip_code_prefix  as customer_zip_code_prefix,
    orders.order_status,
    orders.purchased_at,
    orders.approved_at,
    orders.shipped_at,
    orders.delivered_at,
    orders.estimated_delivery_at,
    coalesce(items.item_count, 0)              as item_count,
    coalesce(items.seller_count, 0)            as seller_count,
    coalesce(items.items_value, 0)             as items_value,
    coalesce(items.freight_value, 0)           as freight_value,
    coalesce(payments.payment_count, 0)        as payment_count,
    coalesce(payments.total_payment_value, 0)  as total_payment_value,
    payments.max_installments,
    reviews.review_score,
    {{ days_between('orders.purchased_at', 'orders.delivered_at') }} as delivery_days,
    case
        when orders.delivered_at is null then null
        else orders.delivered_at > orders.estimated_delivery_at
    end as is_delivered_late
from orders
left join customers on orders.customer_id = customers.customer_id
left join items     on orders.order_id = items.order_id
left join payments  on orders.order_id = payments.order_id
left join reviews   on orders.order_id = reviews.order_id