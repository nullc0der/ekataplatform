from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TaigaIssue(models.Model):
    posted_by = models.ForeignKey(User, related_name='taigaissues')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    posted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.subject
