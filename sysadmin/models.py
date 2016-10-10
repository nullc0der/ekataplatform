from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField

# Create your models here.


class EmailUpdate(models.Model):
    to_users = models.ManyToManyField(User)
    subject = models.CharField(max_length=100)
    message = MarkdownxField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return "Email: %s" % self.id
