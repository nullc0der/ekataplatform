from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class VersionInfo(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, help_text='bg-colorname')
    version_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        get_latest_by = 'id'


class ActiveMemberCount(models.Model):
    date = models.DateField()
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return "%s/%s/%s" % (self.date.day, self.date.month, self.date.year)


class NewMemberCount(models.Model):
    count = models.IntegerField(default=0)
    date = models.DateField()

    def __unicode__(self):
        return "%s/%s/%s" % (self.date.day, self.date.month, self.date.year)


class TotalMemberCount(models.Model):
    count = models.IntegerField(default=0)
    date = models.DateField()

    def __unicode__(self):
        return "%s/%s/%s" % (self.date.day, self.date.month, self.date.year)


class TotalMessageCount(models.Model):
    count = models.IntegerField(default=0)
    date = models.DateField()

    def __unicode__(self):
        return "%s/%s/%s" % (self.date.day, self.date.month, self.date.year)
