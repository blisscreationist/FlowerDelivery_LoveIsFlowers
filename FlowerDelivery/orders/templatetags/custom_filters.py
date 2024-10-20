from django import template
import locale
register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='calc_total')
def calc_total(cart_items):
    total = sum(item.quantity * item.product.price for item in cart_items)
    return total

# Установите локаль для форматирования чисел, если это необходимо
#locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

@register.filter
def format_currency(value):
    if value is None:
        return ''
    try:
        formatted = "{:,.2f}".format(value).replace(",", " ")
        return formatted
    except ValueError:
        return value