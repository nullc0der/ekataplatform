from django.utils.translation import ugettext_lazy as _
from django import forms
from useraccount.models import Transaction, RequestUnits


class TransactionForm(forms.ModelForm):
    instruction = forms.CharField(label=_('Instruction') ,max_length=200, required=False)
    units = forms.IntegerField(label=_('Amount'), min_value=1, max_value=10000)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(TransactionForm, self).__init__(*args, **kwargs)

    def clean_units(self):
        units = self.cleaned_data['units']
        if units > self.request.user.useraccount.balance:
            raise forms.ValidationError(_("Amount can't exceed your balance"))
        return units

    class Meta:
        model = Transaction
        fields = ['instruction', 'units']


class RequestForm(forms.ModelForm):
    instruction = forms.CharField(label=_('Instruction') ,max_length=200, required=False)
    units = forms.IntegerField(label=_('Amount'), min_value=1, max_value=10000)

    class Meta:
        model = RequestUnits
        fields = ['instruction', 'units']
