from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=200, unique=True)
    subscribers = models.ManyToManyField(User)
    unsubscribers = models.ManyToManyField(
        User, related_name='unsubscribed_rooms')
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.name


class Message(models.Model):
    user = models.ForeignKey(User)
    to_user = models.ForeignKey(
        User,
        related_name='recieved_messages',
        null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, related_name='messages')
    content = models.TextField()
    read = models.BooleanField(default=False)
