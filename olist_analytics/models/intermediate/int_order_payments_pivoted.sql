{% set payment_types = ['credit_card', 'boleto', 'voucher', 'debit_card', 'not_defined'] %}

select
    order_id,
    count(*)                    as payment_count,
    max(payment_installments)   as max_installments,
    sum(payment_value)          as total_payment_value,
    {% for p in payment_types %}
    sum(case when payment_type = '{{ p }}' then payment_value else 0 end) as {{ p }}_value
    {%- if not loop.last %},{% endif %}
    {% endfor %}
from {{ ref('stg_order_payments') }}
group by order_id