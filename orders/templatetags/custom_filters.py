from django import template

register = template.Library()


@register.filter
def slice(value, arg):
    """Slices a list from the given start index to the end."""
    try:
        start = int(arg)
        return value[start:]
    except (ValueError, TypeError):
        return value
