from django import template

register = template.Library()

@register.filter
def phone_format(number):
    if number and len(number) == 10:  # assuming all phone numbers have 10 digits
        return f"({number[:2]}) {number[2:6]}-{number[6:]}"
    return number
