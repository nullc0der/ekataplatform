from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_contact_email(email, name, subject, message):
    c = {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    }
    email_subject = "New contact request from landing page "
    email_body = "Name: " + name + '\nEmail Address: ' + email + '\nSubject: ' + subject + '\nMessage: ' + message
    email_html = render_to_string('landing/email.html', c)
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "landing@ekata.social",
        ["support@basicincomeproject.org"]
    )
    msg.attach_alternative(email_html, "text/html")

    msg.send(fail_silently=False)
