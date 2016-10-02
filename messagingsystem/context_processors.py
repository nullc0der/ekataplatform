from messagingsystem.models import Message


def unread_message(request):
    if request.user.is_authenticated():
        unread_count = request.user.recieved_messages.filter(
            read=False
            ).count()
    else:
        unread_count = None
    return {'UNREAD_MESSAGE': unread_count}
