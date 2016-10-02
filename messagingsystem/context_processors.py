from messagingsystem.models import Message


def unread_message(request):
    unread_count = request.user.recieved_messages.filter(
        read=False
    ).count()
    return {'UNREAD_MESSAGE': unread_count}
