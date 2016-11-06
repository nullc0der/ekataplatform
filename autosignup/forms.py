from datetime import timedelta

from django import forms
from django.contrib.auth.models import User
from profilesystem.models import UserAddress
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from autosignup.models import EmailVerfication


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
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={'placeholder': 'email id'}))


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
            if now() > emailverfication.timestamp + timedelta(minutes=10):
                raise forms.ValidationError('The code is old reinitiate one')
        except ObjectDoesNotExist:
            raise forms.ValidationError('Code is invalid')
        return self.cleaned_data.get('verification_code')
