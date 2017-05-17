import random

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


@register.simple_tag
def user_initial(user):
    initials = []
    if user.get_full_name():
        name = user.get_full_name().split()
        for n in name:
            initials.append(n[0])
    else:
        initials.append(user.username[0])
    return ''.join(initials)
