from __future__ import unicode_literals

import requests

from django.db import models
from django.utils.crypto import get_random_string

from invitationsystem.tasks import send_invitation

# Create your models here.


def random_string():
    return get_random_string(length=6)


class Invitation(models.Model):
    email = models.CharField(max_length=100)
    invitation_id = models.CharField(
        max_length=300,
        default=random_string,
        editable=False
    )
    approved = models.BooleanField(default=False)
    sent = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if self.approved:
            if not self.sent:
                send_invitation.delay(self.email, self.invitation_id)
                self.sent = True
                payload = {
                    'email': self.email,
                    'api_key': '475195da-682e-464c-a8f6-8f321306fbf3'
                }
                requests.post(
                    'https://ekata.social/setverified/',
                    payload,
                    verify=False
                )
        super(Invitation, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email
