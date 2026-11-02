{% macro state_to_region(state_col) %}
    case
        when {{ state_col }} in ('AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO') then 'North'
        when {{ state_col }} in ('AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE') then 'Northeast'
        when {{ state_col }} in ('DF', 'GO', 'MT', 'MS') then 'Central-West'
        when {{ state_col }} in ('ES', 'MG', 'RJ', 'SP') then 'Southeast'
        when {{ state_col }} in ('PR', 'RS', 'SC') then 'South'
        else 'Unknown'
    end
{% endmacro %}