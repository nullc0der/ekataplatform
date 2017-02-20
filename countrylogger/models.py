from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserCountry(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name
