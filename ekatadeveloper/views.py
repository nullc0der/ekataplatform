import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.conf import settings
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


class ReactIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'react_template.html' if not settings.EKATA_SITE_TYPE\
     == 'local' else 'react_template_local.html'

    def get_context_data(self, **kwargs):
        context = super(ReactIndexView, self).get_context_data(**kwargs)
        if not settings.EKATA_SITE_TYPE == 'local':
            manifest_file = open(
                os.path.join(settings.BASE_DIR,
                            'static/bundles/chunk-manifest.json'))
            manifest_data = manifest_file.read()
            manifest_file.close()
            context['manifest_data'] = manifest_data
        return context
