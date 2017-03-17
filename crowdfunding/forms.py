from django import forms
from django.utils.translation import ugettext_lazy as _
from crowdfunding.models import CrowdFund, PredefinedAmount, ProductFeature,\
    CardsVideo


class PaymentForm(forms.Form):
    fullname = forms.CharField(max_length=250, required=False)
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


class ProductFeatureForm(forms.ModelForm):
    class Meta:
        model = ProductFeature
        exclude = ['crowdfund', 'linked_card']


class CardsVideoForm(forms.ModelForm):
    class Meta:
        model = CardsVideo
        fields = ['video', 'cover']
