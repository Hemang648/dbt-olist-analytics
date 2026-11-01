select
    geolocation_zip_code_prefix        as zip_code_prefix,
    cast(geolocation_lat as double)    as latitude,
    cast(geolocation_lng as double)    as longitude,
    lower(geolocation_city)            as city,
    upper(geolocation_state)           as state
from {{ source('olist', 'geolocation') }}