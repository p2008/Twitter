from django import template

register = template.Library()


@register.filter
def max_30_chars(value):
    if len(value) > 30:
        return value[:30].rsplit(' ', 1)[0].rstrip(' ') + '...'
    else:
        return value

