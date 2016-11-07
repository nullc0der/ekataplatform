from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException


def send_email_verification_code(email, code):
    c = {
        'code': code
    }
    email_subject = "Email verfication code "
    email_body = "Code: " + code
    email_html = render_to_string('autosignup/email.html', c)
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "support@ekata.social",
        [email]
    )
    msg.attach_alternative(email_html, "text/html")

    msg.send(fail_silently=False)


def send_phone_verfication_code(phone_no, code):
    account_sid = settings.EKATA_TWILIO_ACCOUNT_SID
    auth_token = settings.EKATA_TWILIO_AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(
        body='Verfication code: ' + code + '\nvalid for 10 min',
        to=phone_no,
        from_=settings.EKATA_TWILIO_PHONE_NO
    )
