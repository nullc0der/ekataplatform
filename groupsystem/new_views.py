import os

from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from groupsystem.models import BasicGroup


def get_manifest_data():
    manifest_file = open(os.path.join(
        settings.BASE_DIR, 'static/bundles/chunk-manifest.json'))
    manifest_data = manifest_file.read()
    manifest_file.close()
    return manifest_data


class GroupAdminViews(LoginRequiredMixin, View):
    """
    View to return group admins pages
    This view checks if user is a super_admin(owner)
    or admin if not redirected to 403 page
    """

    template_name = 'react_template.html' if not settings.EKATA_SITE_TYPE\
        == 'local' else 'react_template_local.html'

    def get(self, request, group_id):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            if request.user in set(
                    basicgroup.super_admins.all() | basicgroup.admins.all()):
                request.session['basicgroup'] = basicgroup.id
                manifest_data = ""
                if not settings.EKATA_SITE_TYPE == 'local':
                    manifest_data = get_manifest_data()
                return render(
                    request, self.template_name, {
                        'manifest_data': manifest_data})
            else:
                return HttpResponseRedirect('/error/403/')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/error/404/')


class GroupMemberViews(LoginRequiredMixin, View):
    """
    View to return group member pages
    This view checks if user is a member of the
    group if not redirected to 403 page
    """

    template_name = 'react_template.html' if not settings.EKATA_SITE_TYPE\
        == 'local' else 'react_template_local.html'

    def get(self, request, group_id):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            if request.user in set(
                    basicgroup.super_admins.all() |
                    basicgroup.admins.all() |
                    basicgroup.staffs.all() |
                    basicgroup.moderators.all() |
                    basicgroup.members.all()):
                request.session['basicgroup'] = basicgroup.id
                manifest_data = ""
                if not settings.EKATA_SITE_TYPE == 'local':
                    manifest_data = get_manifest_data()
                return render(
                    request, self.template_name, {
                        'manifest_data': manifest_data})
            else:
                return HttpResponseRedirect('/error/403/')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/error/404/')
