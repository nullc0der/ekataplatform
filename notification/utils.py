from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from notification.models import UserNotification
from notification.onesignal import OneSignal


def create_notification(user, ntype, sender=None, sender_id=None, amount=None, group_name=None):
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
    notification_message = RedisMessage(message)
    RedisPublisher(
        facility='realtime_notification',
        users=[user.username]).publish_message(notification_message)
    onesignals = user.onesignals.all()
    if onesignals:
        player_ids = []
        for onesignal in onesignals:
            player_ids.append(onesignal.onesignalid)
        push = OneSignal(message=message, player_ids=player_ids)
        push.send_message()
