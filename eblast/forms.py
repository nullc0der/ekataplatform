from django import forms
from eblast.models import EmailGroup, EmailTemplate


class EmailGroupForm(forms.ModelForm):
    class Meta:
        model = EmailGroup
        fields = '__all__'


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'html_file']


class EmailTemplateEditForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'template']
