from django import template

register = template.Library()

@register.filter
def status(value1, value2):
    try:
        if (value1-value2) >= 0:
            return "CLEAR"
        else:
            return "PROBLEM"
    except:
        pass