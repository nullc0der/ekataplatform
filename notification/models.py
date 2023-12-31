from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class UserNotification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'transfer'),
        (2, 'request'),
        (3, 'release'),
        (4, 'verified'),
        (5, 'unverified'),
        (6, 'connectionreq'),
        (7, 'connectioncancel'),
        (8, 'connectionaccept'),
        (9, 'connectionreject'),
        (10, 'disconnect'),
        (11, 'groupinvite'),
        (12, 'groupjoinrequest'),
        (13, 'systemupdate'),
        (14, 'gcdistribute')
    )
    user = models.ForeignKey(User, related_name='notifications')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(default='', max_length=200)
    sender_id = models.CharField(max_length=200, default='')
    group_name = models.CharField(max_length=200, default='')
    group_id = models.CharField(max_length=200, default='')
    timeline_id = models.CharField(max_length=200, default='')
    amount = models.FloatField(null=True)
    sysupdate_type = models.CharField(max_length=10, default='')
    sysupdate_message = models.CharField(max_length=300, default='')
    sysupdate_timestamp = models.DateTimeField(null=True)
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(User,
                             related_name='usernotifications')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
