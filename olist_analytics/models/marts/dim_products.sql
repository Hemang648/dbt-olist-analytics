with products as (
    select * from {{ ref('stg_products') }}
),

translation as (
    select * from {{ ref('stg_product_category_translation') }}
)

select
    products.product_id,
    products.category_name,
    coalesce(
        translation.category_name_english,
        products.category_name,
        'unknown'
    ) as category_name_english,
    products.name_length,
    products.description_length,
    products.photos_qty,
    products.weight_g,
    products.length_cm,
    products.height_cm,
    products.width_cm,
    products.length_cm * products.height_cm * products.width_cm as volume_cm3
from products
left join translation
    on products.category_name = translation.category_name