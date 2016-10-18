from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from notification.utils import create_notification
from usertimeline.models import UserTimeline

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
    show = models.BooleanField(default=True)
    visible_in_user_timeline = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        super(SystemUpdate, self).save(*args, **kwargs)
        if not self.show:
            if not self.visible_in_user_timeline:
                users = User.objects.all()
                for user in users:
                    usertimeline = UserTimeline(
                        user=user,
                        timeline_type=3,
                        sysupdate=True,
                        sysupdate_type=self.message_type,
                        sysupdate_message=self.message,
                        sysupdate_timestamp=self.timestamp
                    )
                    usertimeline.save()
                    create_notification(
                        user=user,
                        ntype=13,
                        sysupdate_type=self.message_type,
                        sysupdate_message=self.message,
                        sysupdate_timestamp=self.timestamp,
                        timeline_id=usertimeline.id
                    )
                self.visible_in_user_timeline = True

    def __unicode__(self):
        return "Notice: %s" % self.id
