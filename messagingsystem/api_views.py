from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from profilesystem.permissions import IsAuthenticatedLegacy
from messagingsystem.permissions import IsChatRoomSubscriber
from messagingsystem.serializers import ChatRoomSerializer, MessageSerializer
from messagingsystem.models import ChatRoom


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
            serializer = ChatRoomSerializer(chats, many=True)
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
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, chat_id, format=None):
        try:
            chatroom = ChatRoom.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, chatroom)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
