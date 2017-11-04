from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='truncate_at_word')
def truncate_at_word(value):
    b = value.split('git-svn-id', 1)[0]
    return b