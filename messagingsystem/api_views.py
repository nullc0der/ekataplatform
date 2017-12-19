import json

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.core.urlresolvers import reverse

from channels import Group

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from profilesystem.permissions import IsAuthenticatedLegacy
from messagingsystem.permissions import IsChatRoomSubscriber
from messagingsystem.serializers import ChatRoomSerializer, MessageSerializer
from messagingsystem.models import ChatRoom, Message
from dashboard.models import TotalMessageCount


def _make_message_serializable(message):
    data = {}
    user = {
        'id': message.user.id,
        'username': message.user.username,
        'is_online': message.user.profile.online(),
        'user_image_url': message.user.profile.avatar.url if message.user.profile.avatar else "",
        'user_avatar_color': message.user.profile.default_avatar_color,
        'public_url': reverse('publicusers:user', args=[message.user.id, ])
    }
    to_user = {
        'id': message.to_user.id,
        'username': message.to_user.username,
        'is_online': message.to_user.profile.online(),
        'user_image_url': message.to_user.profile.avatar.url if message.to_user.profile.avatar else "",
        'user_avatar_color': message.to_user.profile.default_avatar_color,
        'public_url': reverse('publicusers:user', args=[message.to_user.id, ])
    }
    data["message"] = message.content
    data["timestamp"] = message.timestamp
    data["read"] = message.read
    data["to_user"] = to_user
    data["user"] = user
    data["id"] = message.id
    return data


class ChatRoomsView(APIView):
    """
    View to return all available chat rooms for an user

    * Only logged in user will be able to access this view
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, format=None):
        """
        Returns a list of available chat rooms
        """
        chats = ChatRoom.objects.filter(
            subscribers=request.user
        ).order_by('-date_created')
        if chats:
            datas = []
            for chat in chats:
                data = {}
                otheruser = [user for user in chat.subscribers.all() if user != request.user]
                data["id"] = chat.id
                data["username"] = otheruser[0].username
                data["is_online"] = otheruser[0].profile.online()
                data["unread_count"] = chat.messages.filter(read=False).count()
                if otheruser[0].profile.avatar:
                    data["user_image_url"] = otheruser[0].profile.avatar.url
                else:
                    data["user_image_url"] = ""
                data["user_avatar_color"] = otheruser[0].profile.default_avatar_color
                datas.append(data)
            serializer = ChatRoomSerializer(datas, many=True)
            return Response(serializer.data)
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)


class ChatRoomDetailsView(APIView):
    """
    View to return all messages in a Chat Room

    * Required logged in User

    get:
    Return list of message in the room

    post:
    Create a new message in specified room if the user is a subscriber

    """
    permission_classes = (IsAuthenticatedLegacy, IsChatRoomSubscriber, )

    def get(self, request, chat_id, format=None):
        try:
            chatroom = ChatRoom.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, chatroom)
        messages = chatroom.messages.all().order_by('timestamp')
        datas = []
        for message in messages:
            data = _make_message_serializable(message)
            datas.append(data)
        serializer = MessageSerializer(datas, many=True)
        return Response(serializer.data)

    def post(self, request, chat_id, format=None):
        try:
            chatroom = ChatRoom.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, chatroom)
        if request.data.get('content'):
            message = Message(user=request.user)
            message.content = request.data.get('content')
            message.room = chatroom
            otherusers = []
            for user in chatroom.subscribers.all():
                if user != request.user:
                    otherusers.append(user)
            if otherusers:
                message.to_user = otherusers[0]
            else:
                for user in chatroom.unsubscribers.all():
                    if user != request.user:
                        message.to_user = user
            message.save()
            totalmessagecount, created = TotalMessageCount.objects.get_or_create(
                date=now().date()
            )
            totalmessagecount.count += 1
            totalmessagecount.save()
            data = _make_message_serializable(message)
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                if otherusers:
                    message_dict = {
                        'chatroom': chatroom.id,
                        'message': serializer.data,
                        'add_message': True
                    }
                    for otheruser in otherusers:
                        Group('%s-messages' % otheruser.username).send({
                            'text': json.dumps(message_dict)
                        })
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
