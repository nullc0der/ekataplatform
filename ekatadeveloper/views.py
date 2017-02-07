from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from groupsystem.models import BasicGroup


@login_required
def send_menus(request):
    group = None
    templates = {
        'home': 'sidebar_home.html',
        'apps': 'sidebar_apps.html',
        'community': 'sidebar_community.html',
        'group': 'sidebar_group.html'
    }
    requested_navbar = request.GET.get('navbar')
    groupid = request.GET.get('groupid')
    if groupid:
        group = BasicGroup.objects.get(id=groupid)
    template_name = templates[requested_navbar]
    return render(
        request,
        template_name,
        {
            'group': group
        }
    )
