"""
Filtros personalizados para templates de inventario.
"""
from django import template

register = template.Library()


@register.filter
def abs_value(value):
    """
    Filtro para obtener el valor absoluto de un número.
    """
    try:
        if value is None:
            return 0
        return abs(int(value))
    except (ValueError, TypeError):
        return 0
