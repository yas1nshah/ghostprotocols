from django import template

register = template.Library()


@register.filter
def format_price(value):
    if value >= 10000000:  # 1 crore = 10,000,000
        crores = value // 10000000
        lacs = (value % 10000000) // 100000
        return f"{crores} crore, {lacs} lacs"
    else:
        lacs = value // 100000
        return f"{lacs} lacs"
