from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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
