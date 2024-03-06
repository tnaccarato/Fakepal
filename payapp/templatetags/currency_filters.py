from django import template

register = template.Library()

CURRENCY_SYMBOLS = {
    'GBP': '£',
    'USD': '$',
    'EUR': '€',
}

@register.filter
def currency_symbol(value):
    print(value.upper())
    return CURRENCY_SYMBOLS.get(value.upper(), value)