from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Look up a value in a dict using a variable key (product.id is an int,
    session cart keys are strings, so this handles the str() conversion)."""
    if not dictionary:
        return None
    return dictionary.get(str(key))