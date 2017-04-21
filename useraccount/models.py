from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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


class IncomeRelease(models.Model):
    user = models.ForeignKey(User, related_name='release')
    amount = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username


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


class DistributeVerification(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)


class NextRelease(models.Model):
    datetime = models.DateTimeField()

    class Meta:
        get_latest_by = 'id'


class RequestUnits(models.Model):
    sender = models.ForeignKey(User, related_name='request_from')
    reciever = models.ForeignKey(User, related_name='request_to')
    units = models.PositiveIntegerField()
    instruction = models.CharField(max_length=200, default='', blank=True)
    date = models.DateField(auto_now_add=True)
