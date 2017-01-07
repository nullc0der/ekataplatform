from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def notification_connect(message):
    Group('%s-notifications' % message.user.username).add(
        message.reply_channel
    )


@channel_session_user
def notification_disconnect(message):
    Group("%s-notifications" % message.user.username).discard(
        message.reply_channel
    )
