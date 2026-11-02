with a as (select count(*) as n from {{ ref('stg_orders') }}),
     b as (select count(*) as n from {{ ref('int_orders_enriched') }})

select
    a.n as stg_orders_rows,
    b.n as enriched_rows
from a
cross join b
where a.n != b.n