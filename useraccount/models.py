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


class RequestUnits(models.Model):
    sender = models.ForeignKey(User, related_name='request_from')
    reciever = models.ForeignKey(User, related_name='request_to')
    units = models.PositiveIntegerField()
    instruction = models.CharField(max_length=200, default='', blank=True)
    date = models.DateField(auto_now_add=True)
