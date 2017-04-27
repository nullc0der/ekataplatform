from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

# Create your models here.


class UserTimeline(models.Model):
    TIMELINE_TYPES = (
        (1, 'transfer'),
        (2, 'request'),
        (3, 'release'),
        (4, 'verified'),
        (5, 'unverified'),
        (6, 'connection'),
        (7, 'gcdistribute')
    )
    user = models.ForeignKey(User, related_name='timelines')
    timeline_type = models.IntegerField(choices=TIMELINE_TYPES)
    sender = models.CharField(max_length=200, default='')
    sender_id = models.CharField(max_length=200, default='')
    reciever = models.CharField(max_length=200, default='')
    reciever_id = models.CharField(max_length=200, default='')
    instruction = models.CharField(max_length=200, default='')
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    not_completed = models.BooleanField(default=True)  # for request units
    conn_main = models.CharField(max_length=100, default='')
    conn_sub = models.CharField(max_length=100, default='')
    accepted = models.BooleanField(default=False)  # for connection
    conn_id = models.IntegerField(null=True)
    sysupdate = models.BooleanField(default=False)
    sysupdate_type = models.CharField(max_length=10, default='')
    sysupdate_message = models.CharField(max_length=300, default='')
    sysupdate_timestamp = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.timeline_type) + " " + self.user.username


class TimelineSetting(models.Model):
    user = models.OneToOneField(User, related_name='timelinesetting')
    enabled_filters = JSONField(
        default={'enabled': ["1", "2", "3", "4", "5", "6", "7"]}
    )
    click_counts = JSONField(
        default={'transfer': 0, 'request': 0, 'release': 0, 'verified': 0, 'unverified': 0, 'connection': 0, 'distribution': 0}
    )

    def __unicode__(self):
        return self.user.username + "'s " + "settings"
