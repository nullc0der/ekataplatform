from django import forms
from landing.models import GlobalOgTag


class GlobalOgTagForm(forms.ModelForm):
    class Meta:
        model = GlobalOgTag
        fields = '__all__'
