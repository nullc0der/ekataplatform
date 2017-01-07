from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def messaging_connect(message):
    Group('%s-messages' % message.user.username).add(message.reply_channel)


@channel_session_user
def messaging_disconnect(message):
    Group("%s-messages" % message.user.username).discard(
        message.reply_channel
    )
