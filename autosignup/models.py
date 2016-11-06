from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CommunitySignup(models.Model):
    COMMUNITY_CHOICES = (
        ('grantcoin', 'grantcoin'),
    )
    user = models.ForeignKey(User, related_name='communitysignups')
    community = models.CharField(max_length=100, choices=COMMUNITY_CHOICES)
    step_1_done = models.BooleanField(default=False)
    step_2_done = models.BooleanField(default=False)
    step_3_done = models.BooleanField(default=False)
    additional_step_done = models.BooleanField(default=False)
    signedup = models.BooleanField(default=False)
    failed_auto_signup = models.BooleanField(default=False)
    sent_to_community_staff = models.BooleanField(default=False)
    useremail = models.EmailField(null=True)

    def __unicode__(self):
        return self.user.username + 'on' + self.community


class EmailVerfication(models.Model):
    user = models.ForeignKey(User)
    community_signup = models.ForeignKey(CommunitySignup)
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
