import json
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.db.models import Q

from rest_framework import status
from rest_framework import parsers
from rest_framework.views import APIView
from rest_framework.response import Response

from profilesystem.permissions import IsAuthenticatedLegacy
from groupsystem.serializers import (
    GroupSerializer, GroupMemberSerializer,
    GroupJoinRequestSerializer, GroupNotificationSerializer
)
from groupsystem.models import (
    BasicGroup,
    JoinRequest,
    GroupNotification,
    GroupMemberNotification,
    GroupInvite,
    InviteAccept
)
from groupsystem.forms import CreateGroupForm, EditGroupForm
from groupsystem.tasks import task_create_emailgroup, task_create_notification
from groupsystem.utils import get_serialized_notification
from groupsystem.permissions import IsAdminOfGroup, IsMemberOfGroup
from notification.utils import create_user_notification
from publicusers.api_views import make_user_serializeable


def _make_group_serializable(group, requesting_user):
    data = {
        'id': group.id,
        'group_url': group.get_absolute_url(),
        'name': group.name,
        'description': group.short_about,
        'ldescription': group.long_about,
        'group_type': group.group_type_other
        if group.get_group_type_display() == 'Other'
        else group.get_group_type_display(),
        'header_image_url': group.header_image.url,
        'logo_url': group.logo.thumbnail["92x92"].url,
        'members': [user.username for user in group.members.all()],
        'subscribers': [user.username for user in group.subscribers.all()],
        'auto_approve_post': group.auto_approve_post,
        'auto_approve_comment': group.auto_approve_comment,
        'join_status': group.join_status,
        'flagged_for_deletion': group.flagged_for_deletion,
        'flagged_for_deletion_on': group.flagged_for_deletion_on,
        'user_permission_set': _calculate_subscribed_group(
            group, requesting_user)
    }
    return data


class GroupsView(APIView):
    """
    This view returns all groups

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, format=None):
        basicgroups = BasicGroup.objects.exclude(
            blocked_members__username__contains=request.user.username
        )
        datas = []
        for basicgroup in basicgroups:
            data = _make_group_serializable(basicgroup, request.user)
            try:
                joinrequest = JoinRequest.objects.get(
                    basic_group=basicgroup,
                    user=request.user
                )
                if joinrequest:
                    data['joinrequest_sent'] = True
            except ObjectDoesNotExist:
                data['joinrequest_sent'] = False
            datas.append(data)
        serializer = GroupSerializer(datas, many=True)
        return Response(serializer.data)


class GroupDetailView(APIView):
    """
    This view returns specified group detail

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            data = _make_group_serializable(basicgroup, request.user)
            return Response(data)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


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


def process_join_request(basicgroup, user):
    data = {
        'group_id': basicgroup.id,
        'type': 'join'
    }
    if basicgroup.join_status == 'open':
        basicgroup.members.add(user)
        data['success'] = True
        data['members'] = [user.username for user in basicgroup.members.all()]
    if basicgroup.join_status == 'request':
        joinrequest, created = JoinRequest.objects.get_or_create(
            basic_group=basicgroup,
            user=user
        )
        data['success'] = True
        task_create_notification.delay(joinrequest, basicgroup)
    if basicgroup.join_status == 'closed':
        data['success'] = False
        data['message'] = 'You can join this group by staff invitation only'
    if basicgroup.join_status == 'invite':
        data['success'] = False
        data['message'] = 'You can join this group by invitation only'
    return data


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
                    data = process_join_request(basicgroup, request.user)
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
            basicgroup = form.save()
            basicgroup.super_admins.add(request.user)
            basicgroup.admins.add(request.user)
            basicgroup.members.add(request.user)
            basicgroup.subscribers.add(request.user)
            task_create_emailgroup.delay(basicgroup)
            data = _make_group_serializable(basicgroup, request.user)
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
    if member in basicgroup.staffs.all():
        subscribed_groups.append(106)
    if member in basicgroup.banned_members.all():
        subscribed_groups.append(107)
    if member in basicgroup.blocked_members.all():
        subscribed_groups.append(108)
    return subscribed_groups


class GroupMembersManagementView(APIView):
    """
    This view returns all members in group with
    their role

    * Required logged in user
    * Permission Required
        * Access Admin
    """
    permission_classes = (IsAuthenticatedLegacy, IsAdminOfGroup)

    def get(self, request, group_id, format=None):
        try:
            datas = []
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            request.session['basicgroup'] = basicgroup.id
            members = basicgroup.super_admins.all() |\
                basicgroup.admins.all() |\
                basicgroup.moderators.all() |\
                basicgroup.staffs.all() |\
                basicgroup.members.all() |\
                basicgroup.subscribers.all() |\
                basicgroup.banned_members.all() |\
                basicgroup.blocked_members.all()
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


class GroupMembersView(APIView):
    """
    This view returns all members in group with
    their role

    * Required logged in user
    * Permission Required
        * Member role
    """
    permission_classes = (IsAuthenticatedLegacy, IsMemberOfGroup)

    def get(self, request, group_id, format=None):
        try:
            datas = []
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            request.session['basicgroup'] = basicgroup.id
            members = basicgroup.super_admins.all() |\
                basicgroup.admins.all() |\
                basicgroup.moderators.all() |\
                basicgroup.staffs.all() |\
                basicgroup.members.all()
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


def remove_user_from_role(basicgroup, member):
    basicgroup.super_admins.remove(member)
    basicgroup.admins.remove(member)
    basicgroup.staffs.remove(member)
    basicgroup.moderators.remove(member)
    basicgroup.members.remove(member)
    basicgroup.subscribers.remove(member)


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
    if 106 in subscribed_groups:
        basicgroup.staffs.add(member)
    else:
        basicgroup.staffs.remove(member)
    if 107 in subscribed_groups:
        if member != editor:
            basicgroup.banned_members.add(member)
            remove_user_from_role(basicgroup, member)
    else:
        basicgroup.banned_members.remove(member)
    if 108 in subscribed_groups:
        if member != editor:
            basicgroup.blocked_members.add(member)
            remove_user_from_role(basicgroup, member)
    else:
        basicgroup.blocked_members.remove(member)


class GroupMemberPermission(APIView):
    """
    This view returns roles of the user in
    specified group

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            subscribed_groups = _calculate_subscribed_group(
                basicgroup, request.user)
            return Response(subscribed_groups)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
    permission_classes = (IsAuthenticatedLegacy, IsAdminOfGroup)

    def post(self, request, group_id, member_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
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
    permission_classes = (IsAuthenticatedLegacy, IsAdminOfGroup)

    def get(self, request, group_id, format=None):
        try:
            datas = []
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
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
    permission_classes = (IsAuthenticatedLegacy, IsAdminOfGroup)

    def post(self, request, group_id, request_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            joinrequest = JoinRequest.objects.get(id=request_id)
            accept = request.data.get('accept', None)
            if accept:
                user = joinrequest.user
                basicgroup.members.add(user)
                joinrequest.delete()
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


class GroupSettingsView(APIView):
    """
    This view sends serialized data for
    groups settings page

    * Required
        * Logged in user
        * Admin level permission
    """

    permission_classes = (IsAuthenticatedLegacy, IsAdminOfGroup)
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser)

    def get(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            request.session['basicgroup'] = basicgroup.id
            serializer = GroupSerializer(
                _make_group_serializable(basicgroup, request.user))
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            from_settings = request.data.get('from_settings', False)
            if from_settings:
                basicgroup.auto_approve_comment = request.data.get(
                    'auto_approve_comment') == 'true'
                basicgroup.auto_approve_post = request.data.get(
                    'auto_approve_post') == 'true'
                basicgroup.join_status = request.data.get(
                    'join_status', 'request')
                basicgroup.save()
                return Response(
                    GroupSerializer(_make_group_serializable(
                        basicgroup, request.user)).data
                )
            form = EditGroupForm(
                request.data,
                instance=basicgroup, basicgroup=basicgroup)
            if form.is_valid():
                basicgroup = form.save(commit=False)
                if request.data.get('logo'):
                    basicgroup.logo = request.data.get('logo')
                if request.data.get('header_image'):
                    basicgroup.header_image = request.data.get('header_image')
                basicgroup.save()
                serializer = GroupSerializer(
                    _make_group_serializable(basicgroup, request.user))
                return Response(serializer.data)
            else:
                data = json.loads(form.errors.as_json())
                errors = []
                for k in data:
                    errors.append(
                        k.upper() + ' : ' + data[k][0]['message'])
                return Response(
                    errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class GroupNotificationsView(APIView):
    """
    This view returns all groups notifications
    and let the admin create, update and delete

    * Permission Required:
        * Logged in user
        * Admin role for Create, Update and Delete

    """

    permission_classes = (IsAuthenticatedLegacy, IsAdminOfGroup)

    def get(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            serializer = GroupNotificationSerializer(
                basicgroup.notifications.all().order_by('-id'),
                many=True
            )
            return Response(
                serializer.data
            )
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            serializer = GroupNotificationSerializer(
                data=request.data
            )
            if serializer.is_valid():
                notification = serializer.save(
                    creator=request.user,
                    basic_group=basicgroup
                )
                task_create_notification.delay(notification, basicgroup)
                return Response(
                    serializer.data
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            notification = GroupNotification.objects.get(
                id=request.data.get('id'))
            serializer = GroupNotificationSerializer(
                notification,
                data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            notification = GroupNotification.objects.get(
                id=request.data.get('id')
            )
            notification.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class GroupMemberNotificationView(APIView):
    """
    This view returns all unread group notification
    for the member

    * Permission Required:
        * Logged in user
    """

    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, group_id, format=None):
        try:
            datas = []
            basicgroup = BasicGroup.objects.get(id=group_id)
            notifications = GroupMemberNotification.objects.filter(
                basic_group=basicgroup,
                user=request.user,
                read=False
            )
            for notification in notifications:
                data = get_serialized_notification(notification)
                if data:
                    datas.append(data)
            return Response(datas)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, group_id, format=None):
        try:
            notification_id = request.data.get('id', None)
            notification = GroupMemberNotification.objects.get(
                id=notification_id
            )
            if notification.user == request.user:
                notification.read = True
                notification.save()
                for mainfeed in notification.mainfeed.all():
                    mainfeed.read = True
                    mainfeed.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


def get_platform_users(basicgroup, searchstring):
    final_list = []
    group_members = set(
        basicgroup.super_admins.all() |
        basicgroup.admins.all() |
        basicgroup.moderators.all() |
        basicgroup.staffs.all() |
        basicgroup.members.all() |
        basicgroup.banned_members.all() |
        basicgroup.blocked_members.all())
    platform_users = User.objects.filter(
        Q(username__istartswith=searchstring) |
        Q(first_name__istartswith=searchstring) |
        Q(last_name__istartswith=searchstring)
        )
    for platform_user in platform_users:
        if platform_user not in group_members:
            final_list.append(platform_user)
    return final_list


def get_serialized_platform_user(basicgroup, searchstring):
    datas = []
    platform_users = get_platform_users(basicgroup, searchstring)
    for platform_user in platform_users:
        data = make_user_serializeable(platform_user)
        data['is_invited'] = False
        for invite in platform_user.received_invites.all():
            if invite.basic_group == basicgroup:
                data['is_invited'] = True
        datas.append(data)
    return datas


class InviteMemberView(APIView):
    """
    * Permission Required
        * Logged in user
        * member of group
    """

    permission_classes = (IsAuthenticatedLegacy, IsMemberOfGroup)

    def get(self, request, group_id, format=None):
        """
        This method returns all platform user except member of
        group if the requested user is a member or admin(This
        depends on join_status) of the group
        """
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            group_staffs = set(
                basicgroup.super_admins.all() |
                basicgroup.admins.all() |
                basicgroup.staffs.all())
            group_members = set(
                basicgroup.super_admins.all() |
                basicgroup.admins.all() |
                basicgroup.moderators.all() |
                basicgroup.staffs.all() |
                basicgroup.members.all())
            if basicgroup.join_status == 'invite'\
                    or basicgroup.join_status == 'open'\
                    and request.user in group_members:
                searchstring = request.GET.get('query', None)
                datas = get_serialized_platform_user(basicgroup, searchstring)
                return Response(datas)
            if basicgroup.join_status == 'closed'\
                    or basicgroup.join_status == 'request'\
                    and request.user in group_staffs:
                searchstring = request.GET.get('query', None)
                datas = get_serialized_platform_user(basicgroup, searchstring)
                return Response(datas)
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            group_staffs = set(
                basicgroup.super_admins.all() |
                basicgroup.admins.all() |
                basicgroup.staffs.all())
            group_members = set(
                basicgroup.super_admins.all() |
                basicgroup.admins.all() |
                basicgroup.moderators.all() |
                basicgroup.staffs.all() |
                basicgroup.members.all())
            if basicgroup.join_status == 'invite'\
                    or basicgroup.join_status == 'open'\
                    and request.user in group_members:
                receiver = User.objects.get(id=request.data.get('user_id'))
                groupinvite = GroupInvite(
                    basic_group=basicgroup,
                    sender=request.user,
                    reciever=receiver
                )
                groupinvite.save()
                create_user_notification(receiver, groupinvite)
                return Response('ok')
            if basicgroup.join_status == 'closed'\
                    or basicgroup.join_status == 'request'\
                    and request.user in group_staffs:
                receiver = User.objects.get(id=request.data.get('user_id'))
                groupinvite = GroupInvite(
                    basic_group=basicgroup,
                    sender=request.user,
                    reciever=receiver
                )
                groupinvite.save()
                create_user_notification(receiver, groupinvite)
                return Response('ok')
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class InviteAction(APIView):
    """
    This view is used for accept/deny
    a invitation
    * Permission required
        * Logged in user
    """

    permission_classes = (IsAuthenticatedLegacy, )

    def post(self, request, format=None):
        try:
            groupinvite = GroupInvite.objects.get(
                id=request.data.get('invite_id'))
            message = "You've denied invite"
            if request.data.get('accepted'):
                groupinvite.basic_group.members.add(groupinvite.reciever)
                inviteaccept = InviteAccept(
                    basic_group=groupinvite.basic_group,
                    sender=groupinvite.sender,
                    user=groupinvite.reciever
                )
                inviteaccept.save()
                task_create_notification.delay(
                    inviteaccept, groupinvite.basic_group)
                message = "You've accepted invite"
            groupinvite.delete()
            return Response({'message': message})
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class RequestDeleteGroup(APIView):
    """
    This view is used to request to delete
    a group
    * Permission Required
        * Logged in User
        * User admin of group
    """

    permission_classes = (IsAuthenticatedLegacy, IsAdminOfGroup)

    def post(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            self.check_object_permissions(request, basicgroup)
            if not basicgroup.flagged_for_deletion:
                basicgroup.flagged_for_deletion = True
                basicgroup.flagged_for_deletion_on = now() + timedelta(days=30)
                basicgroup.save()
            return Response(basicgroup.flagged_for_deletion_on)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
