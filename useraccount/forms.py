from datetime import timedelta

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from useraccount.models import Transaction, UserAccount, \
    DistributeVerification, NextRelease, DistributionPhone
from useraccount.utils import get_ekata_units_info, validate_address


class TransactionForm(forms.Form):
    reciever = forms.CharField(
        label=_('Send To'), max_length=200, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Input addess or username'}
        )
    )
    units = forms.FloatField(
        label=_('Amount'), min_value=0.1, max_value=10000,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Enter Amount'}
        )
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(TransactionForm, self).__init__(*args, **kwargs)

    def clean_units(self):
        units = self.cleaned_data['units']
        account_info = get_ekata_units_info(self.request.user.username)
        if units > account_info['balance']:
            raise forms.ValidationError(_("Amount can't exceed your balance"))
        return units

    def clean_reciever(self):
        reciever = self.cleaned_data['reciever']
        try:
            user = User.objects.get(username=reciever)
            if not hasattr(user, 'useraccount'):
                raise forms.ValidationError(
                    _("User is not subscribed to Ekata Units"))
            return reciever
        except ObjectDoesNotExist:
            pass  # Fallback to address
        address_is_valid = validate_address(reciever)
        if not address_is_valid:
            raise forms.ValidationError(_("User/Address doesn't exist"))
        return reciever


class DistributionForm(forms.Form):
    amount = forms.FloatField(
        label=_('Amount'), min_value=0.1, max_value=10000,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Enter Amount(GRT) per Member'}
        )
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        account_info = get_ekata_units_info("")
        total_amount_needed = UserAccount.objects.count() * amount
        if total_amount_needed > account_info['balance']:
            raise forms.ValidationError(
                _(
                    'Total amount needed is ' +
                    'larger than balance, amount needed: {}'.format(total_amount_needed)
                )
            )
        return amount


class CodeVerificationForm(forms.Form):
    code = forms.CharField(required=True, max_length=8)
    amount = forms.CharField(required=True, widget=forms.HiddenInput())

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            distcodeobj = DistributeVerification.objects.get(code=code)
            if now() > distcodeobj.timestamp + timedelta(minutes=2):
                raise forms.ValidationError(
                    _("Code is expired")
                )
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                _("Invalid Code")
            )
        return code


class NextReleaseForm(forms.ModelForm):
    datetime = forms.DateTimeField(
        required=True,
        label='Next Release',
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker'
            }
        )
    )

    class Meta:
        model = NextRelease
        fields = ['datetime']


class DistributionPhoneForm(forms.ModelForm):
    class Meta:
        model = DistributionPhone
        fields = ['phone_number']
