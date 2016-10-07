from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='useraccount')
    balance = models.PositiveIntegerField(default=1024)
    next_release = models.DateTimeField()

    def create_account(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_account = UserAccount(user=user)
            user_account.next_release = user.date_joined + timedelta(minutes=15)
            user_account.save()
    post_save.connect(create_account, sender=User)

    def __unicode__(self):
        return self.user.username


class Transaction(models.Model):
    from_user = models.ForeignKey(User, related_name='transaction_from')
    to_user = models.ForeignKey(User, related_name='transaction_to')
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
