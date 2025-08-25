from django import template

register = template.Library()

@register.filter
def splitlines(value):
    # Splits text into a new lines
    return [line.strip() for line in value.splitlines() if line.strip()]


