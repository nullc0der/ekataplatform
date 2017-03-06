from django import forms
from crowdfunding.models import CrowdFund, PredefinedAmount


class PaymentForm(forms.Form):
    amount = forms.IntegerField(min_value=1, required=True)
    message = forms.CharField(max_length=250, required=False)


class AdminForm(forms.ModelForm):
    class Meta:
        model = CrowdFund
        fields = ['goal', 'active', 'default_note']


class PredefinedAmountForm(forms.ModelForm):
    class Meta:
        model = PredefinedAmount
        fields = ['amount', 'default']
