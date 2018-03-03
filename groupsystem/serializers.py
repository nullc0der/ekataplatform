from rest_framework import serializers
from groupsystem.models import GroupNotification
from publicusers.serializers import UserSerializer


class GroupNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupNotification
        fields = ('id', 'notification', 'created_on', 'is_important')


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    group_url = serializers.CharField()
    name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=False)
    ldescription = serializers.CharField(required=False)
    group_type = serializers.CharField(required=False)
    header_image_url = serializers.CharField(required=False)
    logo_url = serializers.CharField(required=False)
    members = serializers.ListField(required=True)
    subscribers = serializers.ListField(required=True)
    joinrequest_sent = serializers.BooleanField(required=False)
    auto_approve_post = serializers.BooleanField(required=False)
    auto_approve_comment = serializers.BooleanField(required=False)
    join_status = serializers.CharField(required=False)
    flagged_for_deletion = serializers.BooleanField(required=False)
    flagged_for_deletion_on = serializers.DateTimeField(required=False)
    user_permission_set = serializers.ListField(required=False)


class GroupMemberSerializer(serializers.Serializer):
    user = UserSerializer()
    subscribed_groups = serializers.ListField()


class GroupJoinRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    user = UserSerializer()
