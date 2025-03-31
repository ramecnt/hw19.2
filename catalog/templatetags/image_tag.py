from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def image_tag(image_url, width, height):
    return format_html('<img src="{}" width="{}" height="{}"/>', image_url, width, height)
