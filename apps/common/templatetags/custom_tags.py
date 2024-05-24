from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def active_url(request, view_name):
    try:
        url_name = resolve(request.path_info).url_name
    except:
        url_name = ''
    return 'active' if url_name == view_name else ''
