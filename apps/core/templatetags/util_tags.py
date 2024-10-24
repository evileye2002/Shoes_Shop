from django import template
from apps.core.utils import format_number_with_commas, format_datetime_vn

register = template.Library()


@register.filter
def int_comma(value):
    return format_number_with_commas(value)


@register.filter
def split(value, delimiter=","):
    return value.split(delimiter)


@register.filter
def natural_time(value):
    return format_datetime_vn(value)
