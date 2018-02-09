from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def group_notification_connect(message):
    Group('%s-group-notification' % message.user.username).add(
        message.reply_channel)


@channel_session_user
def group_notification_disconnect(message):
    Group("%s-group-notification" % message.user.username).discard(
        message.reply_channel
    )
