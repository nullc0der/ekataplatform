from django import forms
from django.core.exceptions import ObjectDoesNotExist

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from invitationsystem.models import Invitation


class GetInvitationForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Type your email here to get key...',
                'class': 'input-lg'
            }
        )
    )
    captcha = ReCaptchaField(label='', widget=ReCaptchaWidget())


class CheckInvitationForm(forms.Form):
    invitation_id = forms.CharField(label="Key", max_length=6)
    captcha = ReCaptchaField(label='', widget=ReCaptchaWidget())

    def clean_invitation_id(self):
        invitation_id = self.cleaned_data.get('invitation_id')
        try:
            invitation = Invitation.objects.get(invitation_id=invitation_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Invitation key doesn't exist")
        return invitation_id
