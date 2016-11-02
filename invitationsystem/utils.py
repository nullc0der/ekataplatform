from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_invitation_notification_email(email):
    c = {
        'email': email,
    }
    email_subject = "New invitation id request recieved"
    email_body = "Email: " + email
    email_html = render_to_string(
        'invitationsystem/invitationnotificationemail.html',
        c
    )
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "invitation@ekata.social",
        ["support@ekata.social"]
    )
    msg.attach_alternative(email_html, "text/html")

    return msg.send()


def send_invitation_email(email, invitation_id):
    registration_url = "https://" + Site.objects.get_current().domain + '/accounts/signup/'
    c = {
        'email': email,
        'invitation_id': invitation_id,
        'registration_url': registration_url
    }
    email_subject = "Invitation key for ekata beta"
    email_body = "Invitation id: " + invitation_id + "\nRegistration url: " + registration_url
    email_html = render_to_string(
        'invitationsystem/invitationemail.html',
        c
    )
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "invitation@ekata.social",
        [email]
    )
    msg.attach_alternative(email_html, "text/html")

    return msg.send()
