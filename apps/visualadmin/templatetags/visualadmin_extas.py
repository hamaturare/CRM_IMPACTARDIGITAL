# apps/visualadmin/templatetags/visualadmin_extras.py

from django import template

register = template.Library()

@register.filter
def get_next_state_id(option):
    return option.next_state.id if option.next_state else ''
