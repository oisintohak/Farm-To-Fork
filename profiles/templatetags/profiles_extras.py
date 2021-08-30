from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return f'{arg1} {arg2}'
