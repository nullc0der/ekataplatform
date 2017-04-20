from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from useraccount.models import Transaction, RequestUnits
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
    instruction = forms.CharField(
        label=_('Instruction'), max_length=200, required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Add a note/instruction'}
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
        except ObjectDoesNotExist:
            pass  # Fallback to address
        address_is_valid = validate_address(reciever)
        if not address_is_valid:
            raise forms.ValidationError(_("User/Address doesn't exist"))
        return reciever


class RequestForm(forms.ModelForm):
    instruction = forms.CharField(label=_('Instruction'), max_length=200, required=False)
    units = forms.IntegerField(label=_('Amount'), min_value=1, max_value=10000)

    class Meta:
        model = RequestUnits
        fields = ['instruction', 'units']
