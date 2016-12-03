import requests

from django.contrib import admin
from django_object_actions import DjangoObjectActions, takes_instance_or_queryset
from invitationsystem.models import Invitation
from invitationsystem.tasks import send_invitation

# Register your models here.


class InvitationAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_filter = ('approved', 'sent', 'invitation_type')
    actions = ['resend_invitations']
    change_actions = ['resend_invitations']

    @takes_instance_or_queryset
    def resend_invitations(self, request, queryset):
        count = 0
        for invitation in queryset:
            if invitation.approved:
                send_invitation.delay(
                    invitation.email,
                    invitation.invitation_id
                )
                payload = {
                    'email': invitation.email,
                    'api_key': '475195da-682e-464c-a8f6-8f321306fbf3'
                }
                requests.post(
                    'https://ekata.social/setverified/',
                    payload,
                    verify=False
                )
                invitation.sent = True
                invitation.save()
                count += 1
                self.message_user(
                    request,
                    'sent invitation key to %s' % invitation.email
                )
        self.message_user(
            request,
            'Total resend: %s' % count
        )
    resend_invitations.short_description = 'Resend Invitation'
    resend_invitations.label = 'Resend'

admin.site.register(Invitation, InvitationAdmin)
