from __future__ import unicode_literals

from django.db import models

from invitationsystem.tasks import send_invitation

# Create your models here.


class Invitation(models.Model):
    email = models.CharField(max_length=100)
    invitation_id = models.CharField(max_length=300)
    approved = models.BooleanField(default=False)
    sent = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if self.approved:
            if not self.sent:
                send_invitation.delay(self.email, self.invitation_id)
                self.sent = True
        super(Invitation, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email
