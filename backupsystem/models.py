from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Backup(models.Model):
    name = models.CharField(default='', max_length=300, blank=True)
    b_type = models.CharField(default='', max_length=300, blank=True)
    path = models.CharField(default='', max_length=300, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


class NextBackup(models.Model):
    next_on = models.DateTimeField()

    class Meta:
        get_latest_by = 'id'
