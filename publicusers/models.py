from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Thumbs(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    user = models.ForeignKey(User, related_name='thumbs')
    is_public = models.BooleanField(default=True)


class Connection(models.Model):
    sender = models.ForeignKey(User, related_name='connection_sender')
    reciever = models.ForeignKey(User, related_name='connection_reciever')
    created_at = models.DateTimeField(auto_now_add=True)
    connection_type_main = models.CharField(max_length=100)
    connection_type_sub = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Connection"
        verbose_name_plural = "Connections"

    def __unicode__(self):
        return self.sender.username + self.reciever.username
