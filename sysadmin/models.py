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
    from_email = models.EmailField(default="support@ekata.social")
    timestamp = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return "Email: %s" % self.id


class SystemUpdate(models.Model):
    TYPES = (
        ('1', 'warning'),
        ('2', 'info'),
        ('3', 'danger')
    )
    message_type = models.CharField(max_length=2, choices=TYPES)
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    show = models.BooleanField(default=False)

    def __unicode__(self):
        return "Notice: %s" % self.id
