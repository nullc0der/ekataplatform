from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AccountProvider(models.Model):
    name = models.CharField(max_length=100)
    signup_is_open = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class CommunitySignup(models.Model):
    COMMUNITY_CHOICES = (
        ('grantcoin', 'grantcoin'),
    )
    user = models.ForeignKey(User, related_name='communitysignups')
    community = models.CharField(max_length=100, choices=COMMUNITY_CHOICES, editable=False)
    useraddress_in_db = models.TextField(null=True, blank=True)  # ; seperated
    useremail = models.EmailField(null=True, blank=True)
    userphone = models.CharField(max_length=20, default='')
    useraddress_from_twilio = models.TextField(null=True, blank=True)  # ; seperated
    useraddress_from_geoip = models.TextField(null=True, blank=True)  # ; seperated
    userimage = models.ImageField(
        upload_to='community_signup_user_images',
        null=True,
        blank=True
    )
    step_1_done = models.BooleanField(default=False, editable=False)
    step_2_done = models.BooleanField(default=False, editable=False)
    step_3_done = models.BooleanField(default=False, editable=False)
    additional_step_done = models.BooleanField(default=False, editable=False)
    approved = models.BooleanField(default=False, editable=False)
    failed_auto_signup = models.BooleanField(default=False, editable=False)
    sent_to_community_staff = models.BooleanField(default=False, editable=False)
    auto_signup_fail_reason = models.CharField(max_length=200, default='', editable=False)
    email_in_globaldb = models.BooleanField(default=False, editable=False)
    phone_in_globaldb = models.BooleanField(default=False, editable=False)
    data_collect_done = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return self.user.username


class EmailVerfication(models.Model):
    user = models.ForeignKey(User)
    community_signup = models.ForeignKey(CommunitySignup)
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)


class PhoneVerification(models.Model):
    user = models.ForeignKey(User)
    community_signup = models.ForeignKey(CommunitySignup)
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)


class GlobalEmail(models.Model):
    email = models.EmailField(null=True)


class GlobalPhone(models.Model):
    phone = models.CharField(max_length=100, default='')
