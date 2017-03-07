from django import forms
from django.utils.translation import ugettext_lazy as _
from crowdfunding.models import CrowdFund, PredefinedAmount, ProductFeature


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

    def __init__(self, *args, **kwrags):
        self.crowdfund = kwrags.pop('crowdfund', None)
        super(AdminForm, self).__init__(*args, **kwrags)

    def clean_active(self):
        if self.cleaned_data['active'] and self.crowdfund:
            if self.crowdfund.raised >= self.crowdfund.goal:
                raise forms.ValidationError(
                    _("You can't check active once goal is reached")
                )
        return self.cleaned_data['active']

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
        exclude = ['crowdfund']
