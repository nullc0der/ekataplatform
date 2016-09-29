from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

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
    )
    user = models.ForeignKey(User, related_name='notifications')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(default='', max_length=200)
    sender_id = models.CharField(max_length=200, default='')
    group_name = models.CharField(max_length=200, default='')
    amount = models.IntegerField(null=True)
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username
