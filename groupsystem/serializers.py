from rest_framework import serializers
from publicusers.serializers import UserSerializer


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    group_url = serializers.CharField()
    name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=False)
    group_type = serializers.CharField(required=False)
    header_image_url = serializers.CharField(required=False)
    logo_url = serializers.CharField(required=False)
    members = serializers.ListField(required=True)
    subscribers = serializers.ListField(required=True)
    joinrequest_sent = serializers.BooleanField(required=False)


class GroupMemberSerializer(serializers.Serializer):
    user = UserSerializer()
    subscribed_groups = serializers.ListField()
