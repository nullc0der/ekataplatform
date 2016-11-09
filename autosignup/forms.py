import json
from datetime import timedelta
import requests

from django import forms
from django.contrib.auth.models import User
from profilesystem.models import UserAddress
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.widgets import PhonePrefixSelect

from autosignup.models import EmailVerfication, PhoneVerification,\
    CommunitySignup


class UserInfoForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name'
        ]


class AddressForm(forms.ModelForm):
    house_number = forms.CharField(required=True)
    street = forms.CharField(required=True)
    zip_code = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    country = forms.CharField(required=True)

    class Meta:
        model = UserAddress
        fields = [
            'house_number',
            'street',
            'zip_code',
            'city',
            'state',
            'country',
        ]


class EmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'email id'})
    )


class EmailVerficationForm(forms.Form):
    verification_code = forms.CharField(
        required=True,
        help_text='Check your email for verification code',
        max_length=6
    )

    def __init__(self, community_signup, request, *args, **kwargs):
        self.community_signup = community_signup
        self.request = request
        super(EmailVerficationForm, self).__init__(*args, **kwargs)

    def clean_verification_code(self):
        try:
            emailverfication = EmailVerfication.objects.get(
                code=self.cleaned_data.get('verification_code'),
                community_signup=self.community_signup,
                user=self.request.user
            )
            if now() > emailverfication.timestamp + timedelta(minutes=30):
                raise forms.ValidationError('The code is old ask new')
        except ObjectDoesNotExist:
            raise forms.ValidationError('Code is invalid')
        return self.cleaned_data.get('verification_code')


class PhoneForm(forms.Form):
    country = forms.CharField(
        widget=PhonePrefixSelect(),
        required=True
    )
    phone_no = forms.CharField(
        required=True,
        label='Mobile No'
    )

    def clean(self):
        cleaned_data = super(PhoneForm, self).clean()
        phone_no = cleaned_data.get('country') + cleaned_data.get('phone_no')
        lookup_url = 'https://lookups.twilio.com/v1/' +\
            'PhoneNumbers/%s?Type=carrier' % phone_no
        res = requests.get(lookup_url, auth=(
            settings.EKATA_TWILIO_ACCOUNT_SID,
            settings.EKATA_TWILIO_AUTH_TOKEN
        ))
        if res.status_code == 200:
            data = json.loads(res.content)
            if not data['carrier']['type'].lower() == 'mobile':
                raise forms.ValidationError(_('Provide a valid mobile number'))
        else:
            raise forms.ValidationError(_('Something went wrong! Try later'))


class PhoneVerificationForm(forms.Form):
    verification_code = forms.CharField(
        required=True,
        help_text='Check your phone for verification code',
        max_length=6
    )

    def __init__(self, community_signup, request, *args, **kwargs):
        self.community_signup = community_signup
        self.request = request
        super(PhoneVerificationForm, self).__init__(*args, **kwargs)

    def clean_verification_code(self):
        try:
            phoneverfication = PhoneVerification.objects.get(
                code=self.cleaned_data.get('verification_code'),
                community_signup=self.community_signup,
                user=self.request.user
            )
            if now() > phoneverfication.timestamp + timedelta(minutes=30):
                raise forms.ValidationError('The code is old reinitiate one')
        except ObjectDoesNotExist:
            raise forms.ValidationError('Code is invalid')
        return self.cleaned_data.get('verification_code')


class AdditionalStepForm(forms.Form):
    userimage = forms.ImageField(
        label='Image',
        help_text='upload a recent image of yours',
        required=True
    )
