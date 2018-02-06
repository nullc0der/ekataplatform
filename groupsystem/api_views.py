from django.core.files import File
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from guardian.shortcuts import assign_perm, remove_perm

from profilesystem.permissions import IsAuthenticatedLegacy
from groupsystem.serializers import GroupSerializer, GroupMemberSerializer
from groupsystem.models import (
    BasicGroup,
    GroupMemberExtraPerm,
    GroupMemberRole,
    JoinRequest
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
from notification.utils import create_notification
from publicusers.api_views import _make_user_serializeable # TODO: Make this public


def _make_group_serializable(group):
    data = {
        'id': group.id,
        'group_url': group.get_absolute_url(),
        'name': group.name,
        'description': group.short_about,
        'group_type': group.group_type_other
        if group.get_group_type_display() == 'Other'
        else group.get_group_type_display(),
        'header_image_url': group.header_image.url,
        'logo_url': group.logo.thumbnail["92x92"].url,
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
            try:
                joinrequest = JoinRequest.objects.get(
                    basic_group=basicgroup,
                    user=request.user
                )
                data['joinrequest_sent'] = True
            except ObjectDoesNotExist:
                data['joinrequest_sent'] = False
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


class JoinGroupView(APIView):
    """
    View to do join operations on a group

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def post(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            request_type = request.data.get('type')
            if request_type == 'join':
                if request.user not in basicgroup.banned_members.all():
                    joinrequest, created = JoinRequest.objects.get_or_create(
                        basic_group=basicgroup,
                        user=request.user
                    )
                    if created:
                        admins = basicgroup.super_admins.all() | basicgroup.admins.all()
                        for admin in admins:
                            create_notification(
                                user=admin,
                                ntype=12,
                                sender=request.user.username,
                                sender_id=request.user.id,
                                group_name=basicgroup.name,
                                group_id=basicgroup.id
                            )
                    data = {
                        'group_id': basicgroup.id,
                        'type': 'join',
                        'success': True
                    }
                    return Response(data)
                else:
                    data = {
                        'group_id': basicgroup.id,
                        'type': 'join',
                        'success': False,
                        'message': "You're banned from this group"
                    }
                    return Response(data)
            if request_type == 'cancel':
                joinrequest = JoinRequest.objects.get(
                    basic_group=basicgroup,
                    user=request.user
                )
                joinrequest.delete()
                data = {
                    'group_id': basicgroup.id,
                    'type': 'cancel',
                    'success': True
                }
                return Response(data)
            if request_type == 'leave':
                only_superadmin = False
                try:
                    joinrequest = JoinRequest.objects.get(
                        basic_group=basicgroup,
                        user=request.user
                    )
                    joinrequest.delete()
                except ObjectDoesNotExist:
                    if request.user in basicgroup.super_admins.all()\
                       and basicgroup.super_admins.count() == 1:
                        only_superadmin = True
                if not only_superadmin:
                    basicgroup.members.remove(request.user)
                    basicgroup.super_admins.remove(request.user)
                    basicgroup.admins.remove(request.user)
                    basicgroup.moderators.remove(request.user)
                    perm_groups = request.user.groups.filter(
                        name__istartswith=basicgroup.id
                    )
                    for perm_group in perm_groups:
                        request.user.groups.remove(perm_group)
                    groupmemberrole = GroupMemberRole.objects.get(
                        basic_group=basicgroup,
                        user=request.user
                    )
                    groupmemberrole.delete()
                    extraperm = GroupMemberExtraPerm.objects.get(
                        basic_group=basicgroup,
                        user=request.user
                    )
                    for perm in SUPERADMIN_PERMS:
                        if extraperm.__getattribute__(perm[0]):
                            remove_perm(perm[0], request.user, basicgroup)
                    extraperm.delete()
                    if hasattr(basicgroup, 'emailgroup'):
                        emailgroup = basicgroup.emailgroup
                        emailgroup.users.remove(request.user)
                    data = {
                        'group_id': basicgroup.id,
                        'type': 'leave',
                        'success': True
                    }
                    return Response(data)
                else:
                    data = {
                        'group_id': basicgroup.id,
                        'type': 'leave',
                        'success': False,
                        'message': "Sorry you can't leave" +
                                " as you're only superadmin"
                     }
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
        return Response(
            form.errors.as_json(),
            status=status.HTTP_400_BAD_REQUEST
        )


def _calculate_subscribed_group(basicgroup, member):
    subscribed_groups = []
    if member in basicgroup.subscribers.all():
        subscribed_groups.append(101)
    if member in basicgroup.members.all():
        subscribed_groups.append(102)
    if member in basicgroup.super_admins.all():
        subscribed_groups.append(103)
    if member in basicgroup.admins.all():
        subscribed_groups.append(104)
    if member in basicgroup.moderators.all():
        subscribed_groups.append(105)
    if member in basicgroup.banned_members.all():
        subscribed_groups.append(107)
    return subscribed_groups


class GroupMembersView(APIView):
    """
    This view returns all members in group with
    their role

    * Required logged in user
    * Permission Required
        * Access Admin
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, group_id, format=None):
        try:
            datas = []
            basicgroup = BasicGroup.objects.get(id=group_id)
            members = basicgroup.members.all()
            for member in members:
                data = {}
                data['user'] = _make_user_serializeable(member)
                data['subscribed_groups'] = _calculate_subscribed_group(
                    basicgroup, member)
                datas.append(data)
            serializer = GroupMemberSerializer(datas, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
