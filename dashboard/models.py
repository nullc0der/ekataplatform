from __future__ import unicode_literals

from django.db import models


class VersionInfo(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, help_text='bg-colorname')
    version_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        get_latest_by = 'id'
