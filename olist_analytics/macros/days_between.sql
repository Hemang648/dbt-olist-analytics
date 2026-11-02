{% macro days_between(start_ts, end_ts) %}
    date_diff('day', {{ start_ts }}, {{ end_ts }})
{% endmacro %}