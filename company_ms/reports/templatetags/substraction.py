from django import template

register = template.Library()

@register.filter
def substraction(value1, value2):
    try:
        return value1-value2
    except:
        pass