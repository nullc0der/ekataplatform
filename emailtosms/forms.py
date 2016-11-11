from django import forms
from emailtosms.models import Carrier, Verifier


class ConfirmationForm(forms.Form):
    carrier = forms.ModelChoiceField(
        queryset=Carrier.objects.all(),
        required=True
    )
    phone_number = forms.IntegerField(label="Mobile number", required=True)


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
