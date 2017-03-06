from django import forms
from crowdfunding.models import CrowdFund, PredefinedAmount


class PaymentForm(forms.Form):
    amount = forms.IntegerField(min_value=1, required=True)
    message = forms.CharField(max_length=250, required=False)


class AdminForm(forms.ModelForm):
    end_date = forms.DateTimeField(
        required=False,
        label='End Date',
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker'
            }
        )
    )

    class Meta:
        model = CrowdFund
        fields = [
            'goal', 'default_note',
            'thankyou_message', 'introduction',
            'end_date', 'active'
        ]


class PredefinedAmountForm(forms.ModelForm):
    class Meta:
        model = PredefinedAmount
        fields = ['amount', 'default']
