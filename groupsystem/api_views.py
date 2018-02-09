import json

from django.core.files import File
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from channels import Group

from profilesystem.permissions import IsAuthenticatedLegacy
from groupsystem.serializers import (
    GroupSerializer, GroupMemberSerializer,
    GroupJoinRequestSerializer
)
from groupsystem.models import (
    BasicGroup,
    JoinRequest
)
from groupsystem.forms import CreateGroupForm
from groupsystem.tasks import task_create_emailgroup
from notification.utils import create_notification
from publicusers.api_views import make_user_serializeable


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
                return Response(data)
            else:
                basicgroup.subscribers.remove(request.user)
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
                    data = {
                        'group_id': basicgroup.id,
                        'type': 'join',
                        'success': True
                    }
                    websocket_data = {
                        'group_id': basicgroup.id,
                        'req': {
                            'id': joinrequest.id,
                            'user': make_user_serializeable(joinrequest.user)
                        }
                    }
                    for admin in set(
                            basicgroup.super_admins.all() |
                            basicgroup.admins.all()):
                        Group('%s-group-notification' % (admin.username)).send({
                            'text': json.dumps(websocket_data)
                        })
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
                # If group have single owner
                # don't let the user leave ;p
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
                                " as you're only owner"
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
            basicgroup.admins.add(request.user)
            basicgroup.members.add(request.user)
            basicgroup.subscribers.add(request.user)
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
            members = basicgroup.super_admins.all() |\
                basicgroup.admins.all() |\
                basicgroup.moderators.all() |\
                basicgroup.members.all() |\
                basicgroup.subscribers.all() |\
                basicgroup.banned_members.all()
            for member in set(members):
                data = {}
                data['user'] = make_user_serializeable(member)
                data['subscribed_groups'] = _calculate_subscribed_group(
                    basicgroup, member)
                datas.append(data)
            serializer = GroupMemberSerializer(datas, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


def _change_user_role(basicgroup, member, subscribed_groups, editor):
    if 101 in subscribed_groups:
        basicgroup.subscribers.add(member)
    else:
        basicgroup.subscribers.remove(member)
    if 102 in subscribed_groups:
        basicgroup.members.add(member)
    else:
        basicgroup.members.remove(member)
    if 103 in subscribed_groups:
        basicgroup.super_admins.add(member)
    else:
        if basicgroup.super_admins.count() != 1:
            basicgroup.super_admins.remove(member)
    if 104 in subscribed_groups:
        basicgroup.admins.add(member)
    else:
        basicgroup.admins.remove(member)
    if 105 in subscribed_groups:
        basicgroup.moderators.add(member)
    else:
        basicgroup.moderators.remove(member)
    if 107 in subscribed_groups:
        if member != editor:
            basicgroup.banned_members.add(member)
    else:
        basicgroup.banned_members.remove(member)


class GroupMemberChangeRoleView(APIView):
    """
    This view changes groups member roles

    * Required:
        * Logged in user
        * Permission set (TODO: Decide permission set)
    * Returns:
        * member_id: ID of the member in DB
        * subscribed_groups: Members role
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def post(self, request, group_id, member_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            member = User.objects.get(id=member_id)
            subscribed_groups = request.data.get('subscribed_groups', None)
            _change_user_role(
                basicgroup, member, subscribed_groups, request.user)
            data = {
                'subscribed_groups': _calculate_subscribed_group(
                    basicgroup, member),
                'member_id': member.id
            }
            return Response(data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GroupJoinRequestView(APIView):
    """
    This view returns all join request

    * Required:
        * Logged in user
        * Permission set (TODO: Decide permission set)
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, group_id, format=None):
        try:
            datas = []
            basicgroup = BasicGroup.objects.get(id=group_id)
            joinrequests = basicgroup.joinrequest.filter(approved=False)
            for joinrequest in joinrequests:
                data = {
                    'id': joinrequest.id,
                    'user': make_user_serializeable(joinrequest.user)
                }
                datas.append(data)
            serializer = GroupJoinRequestSerializer(datas, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class GroupJoinRequestApproveView(APIView):
    """
    This view approves/denies a join request

    * Required:
        * Logged in user
        * Permission set (TODO: Decide permission set)
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def post(self, request, group_id, request_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            joinrequest = JoinRequest.objects.get(id=request_id)
            accept = request.data.get('accept', None)
            if accept:
                user = joinrequest.user
                basicgroup.members.add(user)
                joinrequest.approved = True
                joinrequest.save()
                data = {
                    'user': make_user_serializeable(user),
                    'subscribed_groups': _calculate_subscribed_group(
                        basicgroup, user)
                }
                serializer = GroupMemberSerializer(data)
                return Response(serializer.data)
            else:
                data = {
                    'request_id': joinrequest.id
                }
                joinrequest.delete()
                return Response(data)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
