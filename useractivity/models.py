from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class FlaggedAccount(models.Model):
    user = models.OneToOneField(User)
    has_avatar = models.BooleanField(default=False)
    has_gc_signup = models.BooleanField(default=False)
    has_address = models.BooleanField(default=False)
    has_name_fields = models.BooleanField(default=False)
    has_socials = models.BooleanField(default=False)
    has_connections = models.BooleanField(default=False)
    has_posts = models.BooleanField(default=False)
    has_messages = models.BooleanField(default=False)

    first_notice_sent_on = models.DateTimeField(
        null=True, blank=True, editable=False)
    second_notice_sent_on = models.DateTimeField(
        null=True, blank=True, editable=False)
    third_notice_sent_on = models.DateTimeField(
        null=True, blank=True, editable=False)

    user_inactive = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.user_inactive:
            self.user.is_active = False
            self.user.save()
        else:
            self.user.is_active = True
            self.user.save()
        super(FlaggedAccount, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username
