from rest_framework import serializers
from messagingsystem.models import Message


class ChatRoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=200, required=True)
    is_online = serializers.BooleanField(default=False)
    unread_count = serializers.IntegerField(default=0)
    user_image_url = serializers.CharField(max_length=200)
    user_avatar_color = serializers.CharField(max_length=200)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
