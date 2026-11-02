with sellers as (
    select * from {{ ref('stg_sellers') }}
),

geo as (
    select * from {{ ref('int_geolocation_by_zip') }}
)

select
    sellers.seller_id,
    sellers.city,
    sellers.state,
    {{ state_to_region('sellers.state') }} as region,
    sellers.zip_code_prefix,
    geo.latitude,
    geo.longitude
from sellers
left join geo
    on sellers.zip_code_prefix = geo.zip_code_prefix