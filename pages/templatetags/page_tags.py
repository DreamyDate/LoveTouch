from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def render_header():
    return render_to_string('pages/header.html')

@register.simple_tag
def render_footer():
    return render_to_string('pages/footer.html')

