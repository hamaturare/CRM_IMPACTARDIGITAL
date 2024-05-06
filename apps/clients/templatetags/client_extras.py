from django import template

register = template.Library()

@register.filter
def phone_format(phone):
    phone = str(phone).replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('+', '')
    if len(phone) <= 10:  # Número sem código do país
        return '({}) {}-{}'.format(phone[:2], phone[2:6], phone[6:])
    elif len(phone) == 11:  # Incluir os números com nono dígito
        return '({}) {}-{}'.format(phone[:2], phone[2:7], phone[7:11])
    return phone  # Retornar o formato original se não corresponder