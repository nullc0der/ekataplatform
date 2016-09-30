from django import forms
from django.core.exceptions import ObjectDoesNotExist

from invitationsystem.models import Invitation


class CheckInvitationForm(forms.Form):
    invitation_id = forms.CharField(max_length=6)

    def clean_invitation_id(self):
        invitation_id = self.cleaned_data.get('invitation_id')
        try:
            invitation = Invitation.objects.get(invitation_id=invitation_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Invitation key doesn't exist")
        return invitation_id
