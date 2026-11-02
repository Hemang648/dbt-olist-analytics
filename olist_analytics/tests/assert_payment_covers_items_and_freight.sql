{{ config(severity='warn') }}

select
    order_id,
    total_payment_value,
    items_value + freight_value as expected_value
from {{ ref('fct_orders') }}
where order_status = 'delivered'
  and abs(total_payment_value - (items_value + freight_value)) > 1