from django import template

register = template.Library()

@register.filter
def get_dict_value(dictionary, key):
    """
    Get a value from a dictionary using a key.
    Usage: {{ dictionary|get_dict_value:key }}
    """
    if not dictionary:
        return ''
    return dictionary.get(key, '')
