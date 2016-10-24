from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from notification.utils import create_notification
from usertimeline.models import UserTimeline

# Create your models here.


class EmailGroup(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name


class EmailUpdate(models.Model):
    FROM_EMAIL_CHOICES = (
        ('support@ekata.social', 'support@ekata.social'),
        ('news@ekata.social', 'news@ekata.social'),
        ('newsletter@ekata.social', 'newsletter@ekata.social'),
    )
    to_groups = models.ManyToManyField(EmailGroup)
    subject = models.CharField(max_length=100)
    message = MarkdownxField()
    from_email = models.EmailField(
        default='support@ekata.social',
        choices=FROM_EMAIL_CHOICES
    )
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
    show = models.BooleanField(default=True)
    visible_in_user_timeline = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return "Notice: %s" % self.id


def send_systemnotification_to_usertimeline(sender, instance, **kwargs):
    if not instance.show:
        if not instance.visible_in_user_timeline:
            users = User.objects.all()
            for user in users:
                usertimeline = UserTimeline(
                    user=user,
                    timeline_type=3,
                    sysupdate=True,
                    sysupdate_type=instance.message_type,
                    sysupdate_message=instance.message,
                    sysupdate_timestamp=instance.timestamp
                )
                usertimeline.save()
                create_notification(
                    user=user,
                    ntype=13,
                    sysupdate_type=instance.message_type,
                    sysupdate_message=instance.message,
                    sysupdate_timestamp=instance.timestamp,
                    timeline_id=usertimeline.id
                )
            instance.visible_in_user_timeline = True
            instance.save()

post_save.connect(send_systemnotification_to_usertimeline, sender=SystemUpdate)
