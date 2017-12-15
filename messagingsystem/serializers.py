from rest_framework import serializers
from messagingsystem.models import Message


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=200, required=True)
    is_online = serializers.BooleanField(default=False)
    user_image_url = serializers.CharField(max_length=200)
    user_avatar_color = serializers.CharField(max_length=200)


class ChatRoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=200, required=True)
    is_online = serializers.BooleanField(default=False)
    unread_count = serializers.IntegerField(default=0)
    user_image_url = serializers.CharField(max_length=200)
    user_avatar_color = serializers.CharField(max_length=200)


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    to_user = UserSerializer()
    user = UserSerializer()
    message = serializers.CharField()
    timestamp = serializers.DateTimeField()
    read = serializers.BooleanField()
