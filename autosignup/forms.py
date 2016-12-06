import json
from datetime import timedelta
import requests

from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from phonenumber_field.widgets import PhonePrefixSelect

from profilesystem.models import UserAddress
from autosignup.models import EmailVerfication, PhoneVerification,\
    CommunitySignup, AccountAddContact


def carrier_lookup(phone_no):
    if cache.get('%s_lookup' % phone_no):
        lookup = cache.get('%s_lookup' % phone_no)
        return lookup
    else:
        lookup_url = 'https://lookups.twilio.com/v1/' +\
            'PhoneNumbers/%s?Type=carrier' % phone_no
        res = requests.get(lookup_url, auth=(
            settings.EKATA_TWILIO_ACCOUNT_SID,
            settings.EKATA_TWILIO_AUTH_TOKEN
        ))
        if res.status_code == 200:
            lookup = json.loads(res.content)
            cache.set('%s_lookup' % phone_no, lookup, 2 * 60 * 60)
            return lookup
        else:
            return None


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
    phone_no = forms.IntegerField(
        required=True,
        label='Mobile No'
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PhoneForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PhoneForm, self).clean()
        phone_no = cleaned_data.get('country') + str(cleaned_data.get('phone_no'))
        if cache.get('%s_phoneretry' % self.request.user.username):
            phoneretry = cache.get('%s_phoneretry' % self.request.user.username)
            if phoneretry['phone'] == phone_no and phoneretry['retry'] > 9:
                if now() < phoneretry['first_attempt_time'] + timedelta(minutes=60):
                    raise forms.ValidationError(_('Max attempt reached! try later'))
                else:
                    lookup = carrier_lookup(phone_no)
                    if lookup:
                        if lookup['carrier']['type'].lower() != 'mobile':
                            raise forms.ValidationError(_('Provide a valid mobile number'))
                    else:
                        raise forms.ValidationError(_('Something went wrong! Try later'))
        else:
            lookup = carrier_lookup(phone_no)
            if lookup:
                if lookup['carrier']['type'].lower() != 'mobile':
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
        help_text='Upload a recent photo of yourself or image proof of identification.',
        required=True
    )


class AccountAddContactForm(forms.ModelForm):
    class Meta:
        model = AccountAddContact
        fields = '__all__'


class CommunitySignupForm(forms.ModelForm):
    class Meta:
        model = CommunitySignup
        fields = [
            'useraddress_in_db',
            'useremail',
            'userphone',
            'referred_by',
            'referral_code',
            'wallet_address',
            'status',
            'is_on_distribution'
        ]
