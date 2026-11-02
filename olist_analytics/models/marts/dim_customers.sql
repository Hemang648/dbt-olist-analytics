with orders as (
    select * from {{ ref('int_orders_enriched') }}
),

geo as (
    select * from {{ ref('int_geolocation_by_zip') }}
),

ranked as (
    select
        *,
        row_number() over (
            partition by customer_unique_id
            order by purchased_at desc, order_id
        ) as rn
    from orders
),

latest_location as (
    select
        customer_unique_id,
        customer_city             as city,
        customer_state            as state,
        customer_zip_code_prefix  as zip_code_prefix
    from ranked
    where rn = 1
),

order_stats as (
    select
        customer_unique_id,
        count(*) as order_count,
        sum(case when order_status = 'delivered' then 1 else 0 end) as delivered_order_count,
        sum(case when order_status = 'delivered' then total_payment_value else 0 end) as lifetime_value,
        min(purchased_at) as first_order_at,
        max(purchased_at) as last_order_at
    from orders
    group by customer_unique_id
)

select
    order_stats.customer_unique_id,
    order_stats.order_count,
    order_stats.delivered_order_count,
    order_stats.delivered_order_count > 1 as is_repeat_customer,
    order_stats.lifetime_value,
    order_stats.first_order_at,
    order_stats.last_order_at,
    latest_location.city,
    latest_location.state,
    latest_location.zip_code_prefix,
    geo.latitude,
    geo.longitude
from order_stats
left join latest_location
    on order_stats.customer_unique_id = latest_location.customer_unique_id
left join geo
    on latest_location.zip_code_prefix = geo.zip_code_prefix