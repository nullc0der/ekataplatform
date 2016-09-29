import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import UserProfile, UserAddress, UserPhone


class UserForm(forms.ModelForm):
    username = forms.CharField()

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        username_regex = re.compile(r'^[\w.@+-]+$')
        if not username_regex.match(username):
            raise forms.ValidationError(
                _('Usernames can only contain letters, digits and @/./+/-/_.'),
            )
        if username == self.request.user.username:
            return username
        else:
            try:
                User.objects.get(username=username)
            except ObjectDoesNotExist:
                return username
        raise forms.ValidationError(_('Username already taken'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class PInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'website',
            'gender',
            'about_me'
        ]


class PhoneForm(forms.ModelForm):
    phone_office = forms.CharField(widget=PhoneNumberPrefixWidget(attrs={'class' : 'selectphone'}))
    phone_home = forms.CharField(widget=PhoneNumberPrefixWidget(attrs={'class' : 'selectphone'}))
    phone_mobile = forms.CharField(widget=PhoneNumberPrefixWidget(attrs={'class' : 'selectphone'}))
    phone_emergency = forms.CharField(widget=PhoneNumberPrefixWidget(attrs={'class' : 'selectphone'}))

    class Meta:
        model = UserPhone
        fields = [
            'phone_office',
            'phone_home',
            'phone_mobile',
            'phone_emergency'
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
