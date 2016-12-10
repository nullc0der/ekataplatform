from django import forms
from django.core.exceptions import ObjectDoesNotExist

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from invitationsystem.models import Invitation

from autosignup.models import ReferralCode, AccountProvider


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
    invitation_id = forms.CharField(
        label="Please enter in your invitation key or referral code",
        max_length=15
    )
    captcha = ReCaptchaField(label='', widget=ReCaptchaWidget())

    def clean_invitation_id(self):
        invitation_id = self.cleaned_data.get('invitation_id')
        try:
            invitation = Invitation.objects.get(invitation_id=invitation_id)
            return invitation_id
        except ObjectDoesNotExist:
            pass  # Fallback to referral code
        try:
            referral_code = ReferralCode.objects.get(code=invitation_id)
            return invitation_id
        except ObjectDoesNotExist:
            pass
        accountprovider = AccountProvider.objects.get(name='grantcoin')
        if accountprovider.invite_code_is_open and invitation_id == accountprovider.invite_code:
            return invitation_id
        else:
            raise forms.ValidationError("Invitation key or Referral code doesn't exist")
        return invitation_id
