from django import forms
from eblast.models import EmailGroup, EmailTemplate, EmailCampaign


class EmailGroupForm(forms.ModelForm):
    class Meta:
        model = EmailGroup
        fields = '__all__'


class EmailGroupEditForm(forms.ModelForm):
    class Meta:
        model = EmailGroup
        exclude = ['name']


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'html_file']


class EmailTemplateEditForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['template']


class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        exclude = ['draft']


class EmailCampaignEditForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        exclude = ['draft', 'campaign_name']


class EmailTestSendForm(forms.Form):
    FROM_EMAIL_CHOICES = (
        ('support@ekata.social', 'support@ekata.social'),
        ('news@ekata.social', 'news@ekata.social'),
        ('newsletter@ekata.social', 'newsletter@ekata.social'),
    )

    test_email = forms.EmailField(label='Send to')
    from_email_id = forms.ChoiceField(choices=FROM_EMAIL_CHOICES)


class EmailSendForm(forms.Form):
    FROM_EMAIL_CHOICES = (
        ('support@ekata.social', 'support@ekata.social'),
        ('news@ekata.social', 'news@ekata.social'),
        ('newsletter@ekata.social', 'newsletter@ekata.social'),
    )

    from_email_id = forms.ChoiceField(choices=FROM_EMAIL_CHOICES)
    to_groups = forms.ModelMultipleChoiceField(queryset=EmailGroup.objects.all())
