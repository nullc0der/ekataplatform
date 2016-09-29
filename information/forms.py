from django import forms
from information.models import Contact
from information.tasks import send_contact_email_task


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def send_email(self):
        send_contact_email_task.delay(
            email=self.cleaned_data['email_address'],
            first=self.cleaned_data['first_name'],
            last=self.cleaned_data['last_name'],
            company=self.cleaned_data['company_name'],
            telephone=self.cleaned_data['telephone_no'],
            comment=self.cleaned_data['comment']
        )
