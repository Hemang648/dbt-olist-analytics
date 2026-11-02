with a as (select count(*) as n from {{ ref('stg_order_items') }}),
     b as (select count(*) as n from {{ ref('fct_order_items') }})

select a.n as stg_rows, b.n as fct_rows
from a
cross join b
where a.n != b.n