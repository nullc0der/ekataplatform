from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import User

from simple_history.models import HistoricalRecords

from groupsystem.models import BasicGroup

# Create your models here.


class AccountProvider(models.Model):
    name = models.CharField(max_length=100)
    signup_is_open = models.BooleanField(default=True)
    basicgroup = models.OneToOneField(BasicGroup, null=True)
    allowed_distance = models.IntegerField(default=20, blank=True)

    def __unicode__(self):
        return self.name


class ApprovedMailTemplate(models.Model):
    accountprovider = models.ForeignKey(
        AccountProvider,
        related_name='mailtemplate'
    )
    template = models.FileField(upload_to='mailtemplate')
    selected = models.BooleanField(default=False)

    def filename(self):
        return os.path.basename(self.template.name)


class CommunitySignup(models.Model):
    COMMUNITY_CHOICES = (
        ('grantcoin', 'grantcoin'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    )
    user = models.ForeignKey(User, related_name='communitysignups')
    community = models.CharField(max_length=100, choices=COMMUNITY_CHOICES, editable=False)
    useraddress_in_db = models.TextField(verbose_name='Address', null=True, blank=True)  # ; seperated
    useremail = models.EmailField(verbose_name='Email', null=True, blank=True)
    userphone = models.CharField(verbose_name='Phone', max_length=20, default='', blank=True)
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
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    distance_db_vs_twilio = models.CharField(max_length=100, default='', editable=False)
    distance_db_vs_geoip = models.CharField(max_length=100, default='', editable=False)
    failed_auto_signup = models.BooleanField(default=False, editable=False)
    sent_to_community_staff = models.BooleanField(default=False, editable=False)
    auto_signup_fail_reason = models.CharField(max_length=200, default='', editable=False)
    data_collect_done = models.BooleanField(default=False, editable=False)
    approval_mail_sent = models.BooleanField(default=False, editable=False)
    history = HistoricalRecords()

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
    signup = models.ManyToManyField(CommunitySignup, related_name='globalemail')


class GlobalPhone(models.Model):
    phone = models.CharField(max_length=100, default='')
    signup = models.ManyToManyField(CommunitySignup, related_name='globalphone')


class AccountAddContact(models.Model):
    organization = models.CharField(
        verbose_name='Name of organization',
        max_length=100
    )
    emailaddress = models.EmailField(verbose_name="Email Address", null=True)
    proposal = models.TextField()

    def __unicode__(self):
        return self.organization

    class Meta:
        verbose_name = 'Account proposal'
