from django import forms
from emailtosms.models import Carrier, Verifier, UserCarrier


class ConfirmationForm(forms.Form):
    carrier = forms.ModelChoiceField(
        queryset=Carrier.objects.all(),
        required=True
    )
    phone_number = forms.IntegerField(
        label="Mobile Number",
        required=True,
        help_text='Country code is automatically added and you do not need to include'
    )


class VerificationForm(forms.Form):
    code = forms.CharField(
        required=True
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        verifier = Verifier.objects.filter(
            user=self.request.user,
            code=self.cleaned_data.get('code')
        )
        if verifier:
            return self.cleaned_data.get('code')
        else:
            raise forms.ValidationError('Invalid code')


class UserCarrierForm(forms.ModelForm):
    emailaddress = forms.EmailField(
        label='Gateway Email Address',
        help_text="Fill this field if you know your carrier's email to sms gateway address",
        required=False
    )

    class Meta:
        model = UserCarrier
        fields = [
            'name',
            'country',
            'emailaddress'
        ]
