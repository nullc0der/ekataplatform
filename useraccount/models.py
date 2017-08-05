from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


from autosignup.models import CommunitySignup

# Create your models here.


class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='useraccount')
    wallet_accont_name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.user.username


class Transaction(models.Model):
    from_user = models.CharField(max_length=200, default='', blank=True)
    to_user = models.CharField(max_length=200, default='', blank=True)
    units = models.PositiveIntegerField()
    instruction = models.CharField(max_length=200, default='', blank=True)
    date = models.DateField(auto_now_add=True)


class UserDistribution(models.Model):
    user = models.ForeignKey(User, related_name='distribution')
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username


class AdminDistribution(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    no_of_accout = models.PositiveIntegerField()
    total_amount = models.FloatField()
    amount_per_user = models.FloatField()
    log_file_path = models.CharField(default='', max_length=500)


class FailedDistributionBatch(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    batch_number = models.IntegerField(null=True)
    signups = models.ManyToManyField(CommunitySignup)


class DistributeVerification(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(max_length=8)
    timestamp = models.DateTimeField(auto_now_add=True)


class NextRelease(models.Model):
    datetime = models.DateTimeField()

    class Meta:
        get_latest_by = 'id'


class DistributionPhone(models.Model):
    phone_number = models.CharField(
        max_length=200, default='', blank=False,
        help_text='please enter phone number with country code e.g +112345678')

    class Meta:
        get_latest_by = 'id'
