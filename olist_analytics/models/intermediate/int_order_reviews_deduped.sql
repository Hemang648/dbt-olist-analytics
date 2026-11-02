with ranked as (
    select
        *,
        row_number() over (
            partition by order_id
            order by review_created_at desc, review_answered_at desc, review_id desc
        ) as rn
    from {{ ref('stg_order_reviews') }}
)

select
    order_id,
    review_id,
    review_score,
    review_created_at
from ranked
where rn = 1