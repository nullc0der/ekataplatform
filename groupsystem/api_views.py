from django.core.files import File
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from guardian.shortcuts import assign_perm

from profilesystem.permissions import IsAuthenticatedLegacy
from groupsystem.serializers import GroupSerializer
from groupsystem.models import (
    BasicGroup,
    GroupMemberExtraPerm,
    GroupMemberRole
)
from groupsystem.forms import CreateGroupForm
from groupsystem.tasks import task_create_emailgroup
from groupsystem.views import (
    SUPERADMIN_PERMS,
    ADMIN_PERMS,
    MODERATOR_PERMS,
    MEMBER_PERMS,
    SUBSCRIBER_PERMS
)


def _make_group_serializable(group):
    data = {
        'id': group.id,
        'group_url': group.get_absolute_url(),
        'name': group.name,
        'description': group.short_about,
        'group_type': group.group_type_other
        if group.get_group_type_display() == 'Other'
        else group.get_group_type_display(),
        # 'header_image_url': group.header_image.thumbnail["300x100"].url,
        'logo_url': group.logo.thumbnail["80x80"].url,
        'members': [user.username for user in group.members.all()],
        'subscribers': [user.username for user in group.subscribers.all()],
    }
    return data


class GroupsView(APIView):
    """
    This view returns all groups

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, format=None):
        basicgroups = BasicGroup.objects.all()
        datas = []
        for basicgroup in basicgroups:
            data = _make_group_serializable(basicgroup)
            datas.append(data)
        serializer = GroupSerializer(datas, many=True)
        return Response(serializer.data)


class GroupSubscribeView(APIView):
    """
    This view will subscribe/unsubscribe user from a group

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def post(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            data = {
                "subscribed": True,
                "username": request.user.username,
                "group_id": basicgroup.id
            }
            if request.data.get('subscribe'):
                basicgroup.subscribers.add(request.user)
                subscriber_group = Group.objects.get(
                    name='%s_subscriber' % basicgroup.id
                )
                request.user.groups.add(subscriber_group)
                return Response(data)        
            else:
                basicgroup.subscribers.remove(request.user)
                subscriber_group = Group.objects.get(
                    name='%s_subscriber' % basicgroup.id
                )
                request.user.groups.remove(subscriber_group)
                data["subscribed"] = False
                return Response(data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateGroupView(APIView):
    """
    View to create a group

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def post(self, request, format=None):
        form = CreateGroupForm(request.data)
        if form.is_valid():
            basicgroup = form.save(commit=False)
            logo = open('media/group_logo/default.png', 'r')
            basicgroup.logo = File(logo)
            basicgroup.save()
            logo.close()
            basicgroup.super_admins.add(request.user)
            basicgroup.members.add(request.user)
            basicgroup.subscribers.add(request.user)
            super_admin_group = Group.objects.create(
                name='%s_superadmin' % basicgroup.id
            )
            admin_group = Group.objects.create(
                name='%s_admin' % basicgroup.id
            )
            moderator_group = Group.objects.create(
                name='%s_moderator' % basicgroup.id
            )
            member_group = Group.objects.create(
                name='%s_member' % basicgroup.id
            )
            subscriber_group = Group.objects.create(
                name='%s_subscriber' % basicgroup.id
            )
            for perm in SUPERADMIN_PERMS:
                assign_perm(perm[0], super_admin_group, basicgroup)
            for perm in ADMIN_PERMS:
                assign_perm(perm[0], admin_group, basicgroup)
            for perm in MODERATOR_PERMS:
                assign_perm(perm[0], moderator_group, basicgroup)
            for perm in MEMBER_PERMS:
                assign_perm(perm[0], member_group, basicgroup)
            for perm in SUBSCRIBER_PERMS:
                assign_perm(perm[0], subscriber_group, basicgroup)
            request.user.groups.add(super_admin_group)
            groupmemberrole = GroupMemberRole(basic_group=basicgroup)
            groupmemberrole.user = request.user
            groupmemberrole.role_name = 'superadmin'
            groupmemberrole.save()
            extraperm = GroupMemberExtraPerm(basic_group=basicgroup)
            extraperm.user = request.user
            for perm in SUPERADMIN_PERMS:
                setattr(extraperm, perm[0], True)
            extraperm.save()
            task_create_emailgroup.delay(basicgroup)
            data = _make_group_serializable(basicgroup)
            serialized_data = GroupSerializer(data)
            return Response(serialized_data.data)
        else:
            return Response(
                form.errors.as_json(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
