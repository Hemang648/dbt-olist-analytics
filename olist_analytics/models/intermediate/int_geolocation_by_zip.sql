select
    zip_code_prefix,
    avg(latitude)  as latitude,
    avg(longitude) as longitude,
    mode(state)    as state,
    count(*)       as point_count
from {{ ref('stg_geolocation') }}
group by zip_code_prefix