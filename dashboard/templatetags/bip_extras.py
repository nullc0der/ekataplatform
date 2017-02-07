from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def active(request, url, args=None):
    if args:
        u = reverse(url, args=[args, ])
    else:
        u = reverse(url)
    if request.path == u:
        return 'active'
    return ''
