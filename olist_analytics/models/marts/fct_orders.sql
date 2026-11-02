{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

select *
from {{ ref('int_orders_enriched') }}

{% if is_incremental() %}
where purchased_at >= (select max(purchased_at) from {{ this }})
                      - interval '{{ var("orders_lookback_days", 30) }} days'
{% endif %}