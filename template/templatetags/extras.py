from django import template

register = template.Library()


@register.filter(name='inc')
def inc(digit, adding):
    return int(digit) + int(adding)


@register.simple_tag
def division(a, b, to_int=False):
    a = int(a)
    b = int(b)
    if to_int:
        result = int(a / b)
    else:
        result = a / b
    return result
