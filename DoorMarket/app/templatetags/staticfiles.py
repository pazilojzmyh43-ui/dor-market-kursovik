"""Совместимость с шаблонами Visual Studio 2019: {% load staticfiles %}."""
from django import template
from django.templatetags.static import do_static

register = template.Library()
register.tag('static', do_static)
