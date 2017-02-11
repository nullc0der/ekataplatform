import json
from datetime import timedelta
import requests

from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.core.validators import RegexValidator
from phonenumber_field.widgets import PhonePrefixSelect

from profilesystem.models import UserAddress
from autosignup.models import EmailVerfication, PhoneVerification,\
    CommunitySignup, AccountAddContact, ReferralCode


alphanumeric_validator = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.'
)


def referral_code_length_validator(val):
    if len(val) != 10:
        raise ValidationError(
            "Referral code must be 10 char long"
        )


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


class ReferralCodeForm(forms.Form):
    referral_code = forms.CharField(
        label='Referral Code',
        max_length=40,
        required=False,
        help_text='If someone gave you a referral code please enter it here'
    )

    def clean_referral_code(self):
        if self.cleaned_data.get('referral_code'):
            try:
                referral_code = ReferralCode.objects.get(code=self.cleaned_data.get('referral_code'))
            except ObjectDoesNotExist:
                raise forms.ValidationError('Code is invalid')
        return self.cleaned_data.get('referral_code')


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

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PhoneForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PhoneForm, self).clean()
        phone_no = cleaned_data.get('country') + str(cleaned_data.get('phone_no'))
        phone_no = phone_no.split('-')
        phone_no = "".join(phone_no)
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
            'useremail',
            'userphone',
            'wallet_address',
            'status',
            'is_on_distribution'
        ]


class ReferralCodeEditForm(forms.Form):
    referral_code = forms.CharField(
        label='Referral Code',
        max_length=40,
        required=False,
        validators=[alphanumeric_validator, referral_code_length_validator]
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ReferralCodeEditForm, self).__init__(*args, **kwargs)

    def clean_referral_code(self):
        referral_code = self.cleaned_data.get('referral_code')
        if referral_code:
            try:
                rcode_obj = ReferralCode.objects.get(code=referral_code)
                if rcode_obj.user == self.user:
                    return referral_code
                else:
                    raise forms.ValidationError(
                        "This code is used"
                    )
            except ObjectDoesNotExist:
                return referral_code
        return referral_code
