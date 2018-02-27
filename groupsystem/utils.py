import json
import requests
from datetime import timedelta

from django.contrib.auth.models import User
from django.core import serializers
from django.utils.timezone import now

from channels import Group

from publicusers.api_views import make_user_serializeable
from eblast.models import EmailGroup
from groupsystem.models import (
    BasicGroup, JoinRequest, GroupMemberNotification,
    GroupNotification, InviteAccept
)


def default(obj):
    import datetime

    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError('Not sure how to serialize %s' % (obj,))


def create_emailgroup(basicgroup):
    emailgroup, created = EmailGroup.objects.get_or_create(
        name=basicgroup.name,
        basic_group=basicgroup
    )
    for user in basicgroup.super_admins.all():
        emailgroup.users.add(user)
    for user in basicgroup.admins.all():
        emailgroup.users.add(user)
    for user in basicgroup.moderators.all():
        emailgroup.users.add(user)
    for user in basicgroup.members.all():
        emailgroup.users.add(user)

    return 1


def send_serialized_user(pk_set):
    users = User.objects.filter(id__in=pk_set)
    data = serializers.serialize('json', users)
    payload = {'data': data}
    url = 'https://development.ekata.social/en/type/integrate_users/'
    res = requests.post(url, data=payload)
    return res.status_code


def create_notification(obj, basicgroup):
    if isinstance(obj, JoinRequest):
        for admin in set(
                basicgroup.super_admins.all() | basicgroup.admins.all()):
            group_member_notification = GroupMemberNotification(
                basic_group=basicgroup,
                user=admin,
                content_object=obj
            )
            group_member_notification.save()
            websocket_data = {
                'group_id': basicgroup.id,
                'notification': get_serialized_notification(
                    group_member_notification)
            }
            Group('%s-group-notification' % (admin.username)).send({
                'text': json.dumps(websocket_data)
            })
    if isinstance(obj, GroupNotification):
        for member in set(
                basicgroup.super_admins.all() | basicgroup.admins.all() |
                basicgroup.staffs.all() | basicgroup.moderators.all() |
                basicgroup.members.all()):
            group_member_notification = GroupMemberNotification(
                basic_group=basicgroup,
                user=member,
                content_object=obj
            )
            group_member_notification.save()
            websocket_data = {
                'group_id': basicgroup.id,
                'notification': get_serialized_notification(
                    group_member_notification)
            }
            Group('%s-group-notification' % (member.username)).send({
                'text': json.dumps(websocket_data, default=default)
            })
    if isinstance(obj, InviteAccept):
        for admin in set(
                basicgroup.super_admins.all() | basicgroup.admins.all()):
            group_member_notification = GroupMemberNotification(
                basic_group=basicgroup,
                user=admin,
                content_object=obj
            )
            group_member_notification.save()
            websocket_data = {
                'group_id': basicgroup.id,
                'notification': get_serialized_notification(
                    group_member_notification)
            }
            Group('%s-group-notification' % (admin.username)).send({
                'text': json.dumps(websocket_data)
            })


def get_serialized_notification(notification):
    data = {}
    if notification.content_object:
        if isinstance(notification.content_object, JoinRequest):
            joinrequest = notification.content_object
            data['type'] = 'joinrequest'
            data['joinrequest_id'] = joinrequest.id
            data['user'] = make_user_serializeable(joinrequest.user)
            data['notification_id'] = notification.id
        if isinstance(notification.content_object, GroupNotification):
            group_notification = notification.content_object
            data['type'] = 'groupnotification'
            data['notification_id'] = notification.id
            data['group_notification_id'] = group_notification.id
            data['notification'] = group_notification.notification
            data['created_on'] = group_notification.created_on
        if isinstance(notification.content_object, InviteAccept):
            group_invite = notification.content_object
            data['type'] = 'inviteaccept'
            data['notification_id'] = notification.id
            data['sender'] = make_user_serializeable(group_invite.sender)
            data['member'] = make_user_serializeable(group_invite.user)
    return data


def process_flagged_for_delete_group():
    for basicgroup in BasicGroup.objects.all():
        if basicgroup.flagged_for_deletion\
                and basicgroup.flagged_for_deletion_on > now():
            basicgroup.delete()
