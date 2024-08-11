from django import template
import math

register = template.Library()

@register.filter
def split(value, separator):
    return value.split(separator)

@register.filter
def subtract(value, arg):
    return int(value) - int(arg)

@register.filter
def fraction_times_100_one_minus(value):
    try:
        fractional_part = value - math.floor(value)
        return (1-fractional_part) * 100
    except (ValueError, TypeError):
        return 0