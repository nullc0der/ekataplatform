from django import forms
from crowdfunding.models import CrowdFund


class PaymentForm(forms.Form):
    amount = forms.IntegerField(min_value=1, required=True)
    message = forms.CharField(max_length=250, required=False)


class AdminForm(forms.ModelForm):
    class Meta:
        model = CrowdFund
        fields = ['goal', 'active']
