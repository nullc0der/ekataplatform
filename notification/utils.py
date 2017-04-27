import json
from django.template import loader
from channels import Group
from notification.models import UserNotification
from notification.onesignal import OneSignal


def create_notification(
    user,
    ntype,
    sender=None,
    sender_id=None,
    amount=None,
    group_name=None,
    timeline_id=None,
    group_id=None,
    sysupdate_type=None,
    sysupdate_message=None,
    sysupdate_timestamp=None
):
    notification = UserNotification(user=user)
    notification.notification_type = ntype
    if sender:
        notification.sender = sender
    if sender_id:
        notification.sender_id = sender_id
    if amount:
        notification.amount = amount
    if group_name:
        notification.group_name = group_name
    if group_id:
        notification.group_id = group_id
    if timeline_id:
        notification.timeline_id = timeline_id
    if sysupdate_type:
        notification.sysupdate_type = sysupdate_type
    if sysupdate_message:
        notification.sysupdate_message = sysupdate_message
    if sysupdate_timestamp:
        notification.sysupdate_timestamp = sysupdate_timestamp
    notification.save()
    if ntype == 1:
        message = "%s sent %s units" % (sender, amount)
    if ntype == 2:
        message = "%s requested %s units" % (sender, amount)
    if ntype == 3:
        message = "%s units released" % amount
    if ntype == 4:
        message = "%s verified you" % sender
    if ntype == 5:
        message = "%s unverified you" % sender
    if ntype == 6:
        message = "%s sent you connection request" % sender
    if ntype == 7:
        message = "%s canceled connection request" % sender
    if ntype == 8:
        message = "%s accepted your connection request" % sender
    if ntype == 9:
        message = "%s rejected your connection request" % sender
    if ntype == 10:
        message = "%s disconnected from you" % sender
    if ntype == 11:
        message = "%s invited you to %s" % (sender, group_name)
    if ntype == 12:
        message = "%s sent a join request to group %s" % (sender, group_name)
    if ntype == 13:
        message = "New system notification published"
    if ntype == 14:
        message = "%s GRT distributed to your account" % amount
    try:
        Group('%s-notifications' % user.username).send({
            "text": message
        })
    except:
        pass
    onesignals = user.onesignals.all()
    if onesignals:
        player_ids = []
        for onesignal in onesignals:
            player_ids.append(onesignal.onesignalid)
        push = OneSignal(message=message, player_ids=player_ids)
        push.send_message()
