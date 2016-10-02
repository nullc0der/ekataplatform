from __future__ import unicode_literals
import uuid

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage

# Create your models here.


class BasicGroup(models.Model):
    GROUP_TYPES = (
        ('1', _('Art')),
        ('2', _('Activist')),
        ('3', _('Political')),
        ('4', _('News')),
        ('5', _('Business')),
        ('6', _('Government')),
        ('7', _('Blog')),
        ('8', _('Other')),
    )
    name = models.CharField(max_length=40)
    short_about = models.CharField(max_length=300)
    long_about = models.TextField(null=True, blank=True)
    group_type = models.CharField(max_length=30, choices=GROUP_TYPES)
    group_type_other = models.CharField(
        verbose_name=_('Please Specify'),
        max_length=30,
        null=True,
        blank=True
    )
    header_image = VersatileImageField(
        upload_to='group_headers',
        null=True,
        blank=True,
        placeholder_image=OnStoragePlaceholderImage(
            path='group_header/default.png'
        )
    )
    logo = VersatileImageField(
        upload_to='group_logos',
        null=True,
        blank=True,
        placeholder_image=OnStoragePlaceholderImage(
            path='group_logo/default.png'
        )
    )
    group_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    super_admins = models.ManyToManyField(User, related_name='basicgroups')
    members = models.ManyToManyField(User, related_name='joined_group')
    subscribers = models.ManyToManyField(User, related_name='subscribed_group')
    banned_members = models.ManyToManyField(User, related_name='banned_group')
    default_roles = models.TextField(
        default='superadmin;admin;moderator;member;subscriber',
        editable=False
    )  # seperated by ';' from higher permission level to lower
    created_on = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('g:groupdetails', args=[self.id, ])

    def get_settings_url(self):
        return reverse('g:adminsettings', args=[self.id, ])

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('can_access_admin', _("Can access admin")),
            ('can_read_news', _("Can read news")),
            ('can_create_news', _("Can create news")),
            ('can_update_news', _("Can update news")),
            ('can_delete_news', _("Can delete news")),
            ('can_read_post', _("Can read post")),
            ('can_create_post', _("Can create post")),
            ('can_update_post', _("Can update post")),
            ('can_approve_post', _("Can approve post")),
            ('can_delete_post', _("Can delete post")),
            ('can_read_comment', _("Can read comment")),
            ('can_create_comment', _("Can create comment")),
            ('can_update_comment', _("Can update comment")),
            ('can_approve_comment', _("Can approve comment")),
            ('can_delete_comment', _("Can delete comment")),
            ('can_like_post', _("Can like post")),
            ('can_create_notification', _("Can create notification")),
            ('can_create_invite', _("Can create invite")),
            ('can_add_member', _("Can add member")),
            ('can_remove_member', _("Can remove member")),
            ('can_ban_member', _("Can ban member")),
            ('can_lift_member_ban', _("Can lift member ban")),
            ('can_change_member_role', _("Can change member role")),
            ('can_edit_member_permission', _("Can edit member permission")),
            ('can_read_events', _("Can read events")),
            ('can_create_events', _("Can create events")),
            ('can_update_events', _("Can update events")),
            ('can_delete_events', _("Can delete events")),
            ('can_read_joinrequest', _("Can read join requests")),
            ('can_approve_joinrequest', _("Can approve join requests")),
            ('can_deny_joinrequest', _("Can deny joinrequest")),
            ('can_edit_group_profile', _("Can edit group profile")),
            ('can_read_role', _("Can read role")),
            ('can_read_custom_role', _("Can read custom role")),
            ('can_update_custom_role', _("Can update custom role")),
            ('can_create_custom_role', _("Can create custom role")),
        )


class GroupNews(models.Model):
    creator = models.ForeignKey(User)
    basic_group = models.ForeignKey(BasicGroup, related_name='news')
    news = models.TextField(verbose_name='Content')
    title = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)


class GroupPost(models.Model):
    creator = models.ForeignKey(User)
    basic_group = models.ForeignKey(BasicGroup, related_name='posts')
    post = models.TextField()
    title = models.CharField(max_length=200)
    admin_created = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='approved_posts', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    commentor = models.ForeignKey(User)
    post = models.ForeignKey(GroupPost, related_name='comments')
    basic_group = models.ForeignKey(BasicGroup, related_name='postcomments', null=True)
    comment = models.TextField()
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='approved_comments', null=True, blank=True)
    commented_on = models.DateTimeField(auto_now_add=True)


class PostLikes(models.Model):
    liker = models.ForeignKey(User)
    post = models.ForeignKey(GroupPost, related_name='likes')
    liked_on = models.DateTimeField(auto_now_add=True)


class GroupNotification(models.Model):
    creator = models.ForeignKey(User)
    basic_group = models.ForeignKey(BasicGroup, related_name='notifications')
    notification = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)


class GroupInvite(models.Model):
    basic_group = models.ForeignKey(BasicGroup, related_name='invites')
    sender = models.ForeignKey(User, related_name='sent_invites')
    reciever = models.ForeignKey(User, related_name='received_invites')
    sent_on = models.DateTimeField(auto_now_add=True)


class GroupEvent(models.Model):
    creator = models.ForeignKey(User)
    basic_group = models.ForeignKey(BasicGroup, related_name='events')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=60)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    background_color = models.CharField(max_length=10)
    border_color = models.CharField(max_length=10)


class JoinRequest(models.Model):
    basic_group = models.ForeignKey(BasicGroup, related_name='joinrequest')
    user = models.ForeignKey(User)
    approved = models.BooleanField(default=False)


class CustomRole(models.Model):
    basic_group = models.ForeignKey(BasicGroup, related_name='customrole')
    custom_role_name = models.CharField(max_length=50, default='', blank=False)
    permission_group = models.CharField(max_length=100, default='')
    can_access_admin = models.BooleanField(default=False)
    can_read_news = models.BooleanField(default=False)
    can_create_news = models.BooleanField(default=False)
    can_update_news = models.BooleanField(default=False)
    can_delete_news = models.BooleanField(default=False)
    can_read_post = models.BooleanField(default=False)
    can_create_post = models.BooleanField(default=False)
    can_update_post = models.BooleanField(default=False)
    can_approve_post = models.BooleanField(default=False)
    can_delete_post = models.BooleanField(default=False)
    can_read_comment = models.BooleanField(default=False)
    can_create_comment = models.BooleanField(default=False)
    can_update_comment = models.BooleanField(default=False)
    can_approve_comment = models.BooleanField(default=False)
    can_delete_comment = models.BooleanField(default=False)
    can_like_post = models.BooleanField(default=False)
    can_create_notification = models.BooleanField(default=False)
    can_create_invite = models.BooleanField(default=False)
    can_add_member = models.BooleanField(default=False)
    can_remove_member = models.BooleanField(default=False)
    can_ban_member = models.BooleanField(default=False)
    can_lift_member_ban = models.BooleanField(default=False)
    can_change_member_role = models.BooleanField(default=False)
    can_edit_member_permission = models.BooleanField(default=False)
    can_read_events = models.BooleanField(default=False)
    can_create_events = models.BooleanField(default=False)
    can_update_events = models.BooleanField(default=False)
    can_delete_events = models.BooleanField(default=False)
    can_read_joinrequest = models.BooleanField(default=False)
    can_approve_joinrequest = models.BooleanField(default=False)
    can_deny_joinrequest = models.BooleanField(default=False)
    can_edit_group_profile = models.BooleanField(default=False)
    can_read_role = models.BooleanField(default=False)
    can_read_custom_role = models.BooleanField(default=False)
    can_update_custom_role = models.BooleanField(default=False)
    can_create_custom_role = models.BooleanField(default=False)


class GroupMemberRole(models.Model):
    basic_group = models.ForeignKey(BasicGroup, related_name='memberrole')
    user = models.ForeignKey(User)
    role_name = models.CharField(max_length=50)


class GroupMemberExtraPerm(models.Model):
    basic_group = models.ForeignKey(BasicGroup, related_name='memberextraperm')
    user = models.ForeignKey(User)
    can_access_admin = models.BooleanField(default=False)
    can_read_news = models.BooleanField(default=False)
    can_create_news = models.BooleanField(default=False)
    can_update_news = models.BooleanField(default=False)
    can_delete_news = models.BooleanField(default=False)
    can_read_post = models.BooleanField(default=False)
    can_create_post = models.BooleanField(default=False)
    can_update_post = models.BooleanField(default=False)
    can_approve_post = models.BooleanField(default=False)
    can_delete_post = models.BooleanField(default=False)
    can_read_comment = models.BooleanField(default=False)
    can_create_comment = models.BooleanField(default=False)
    can_update_comment = models.BooleanField(default=False)
    can_approve_comment = models.BooleanField(default=False)
    can_delete_comment = models.BooleanField(default=False)
    can_like_post = models.BooleanField(default=False)
    can_create_notification = models.BooleanField(default=False)
    can_create_invite = models.BooleanField(default=False)
    can_add_member = models.BooleanField(default=False)
    can_remove_member = models.BooleanField(default=False)
    can_ban_member = models.BooleanField(default=False)
    can_lift_member_ban = models.BooleanField(default=False)
    can_change_member_role = models.BooleanField(default=False)
    can_edit_member_permission = models.BooleanField(default=False)
    can_read_events = models.BooleanField(default=False)
    can_create_events = models.BooleanField(default=False)
    can_update_events = models.BooleanField(default=False)
    can_delete_events = models.BooleanField(default=False)
    can_read_joinrequest = models.BooleanField(default=False)
    can_approve_joinrequest = models.BooleanField(default=False)
    can_deny_joinrequest = models.BooleanField(default=False)
    can_edit_group_profile = models.BooleanField(default=False)
    can_read_role = models.BooleanField(default=False)
    can_read_custom_role = models.BooleanField(default=False)
    can_update_custom_role = models.BooleanField(default=False)
    can_create_custom_role = models.BooleanField(default=False)
