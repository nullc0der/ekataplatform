import bleach
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from profilesystem.models import UserProfile
from groupsystem.models import BasicGroup, GroupPost, PostComment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicGroup
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ('thumbnail', 'thumbnail__82x82')
        ]
    )
    is_online = serializers.SerializerMethodField()
    public_url = serializers.SerializerMethodField()

    def get_is_online(self, obj):
        return obj.online()

    def get_public_url(self, obj):
        return obj.get_public_profile_url()

    class Meta:
        model = UserProfile
        fields = ('avatar', 'default_avatar_color', 'is_online', 'public_url')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    fullname = serializers.SerializerMethodField()

    def get_fullname(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ('id', 'username', 'fullname', 'profile')


class PostSerializer(serializers.ModelSerializer):
    creator = UserSerializer(required=False)
    basic_group = GroupSerializer(required=False)
    approved_by = UserSerializer(required=False)
    created_date = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField(required=False)

    def get_created_date(self, obj):
        return obj.created_on.date()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def validate_post(self, value):
        cleaned_text = bleach.clean(
            value,
            settings.BLEACH_VALID_TAGS,
            settings.BLEACH_VALID_ATTRS,
            settings.BLEACH_VALID_STYLES
        )
        return cleaned_text  # sanitize markdown

    class Meta:
        model = GroupPost
        fields = '__all__'


class CommentSerialzer(serializers.ModelSerializer):
    commentor = UserSerializer(required=False)
    post = PostSerializer(required=False)
    approved_by = UserSerializer(required=False)

    class Meta:
        model = PostComment
        fields = '__all__'
