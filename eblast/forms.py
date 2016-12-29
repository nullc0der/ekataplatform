from django import forms
from eblast.models import EmailGroup


class EmailGroupForm(forms.ModelForm):
    class Meta:
        model = EmailGroup
        fields = '__all__'
