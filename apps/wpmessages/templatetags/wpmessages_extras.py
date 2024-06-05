from django import template

register = template.Library()

@register.filter
def phone_format(phone):
    phone = str(phone).replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('+', '')
    if len(phone) <= 10:  # Número sem código do país e sem ddd
        return '({}) {}-{}'.format(phone[:2], phone[2:6], phone[6:])
    elif len(phone) == 11:  # Incluir os números com nono dígito #Numeros Brasil sem codigo
        return '({}) {}-{}'.format(phone[:2], phone[2:7], phone[7:11])
    elif len(phone) == 12:  # Incluir os números com nono dígito Brasil com 55
        return '+{} ({}) {}-{}'.format(phone[:3],phone[3:6], phone[6:9], phone[9:])
    elif len(phone) == 13:  # Incluir os números com nono dígito Brasil com 55
        return '+{} ({}) {}-{}'.format(phone[:2],phone[2:4], phone[5:9], phone[9:])
    return phone  # Retornar o formato original se não corresponder
