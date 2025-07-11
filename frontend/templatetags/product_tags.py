from django import template

register = template.Library()

@register.filter
def chunks(lst, n):
    """Yield successive n-sized chunks from a list."""
    if lst:
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
