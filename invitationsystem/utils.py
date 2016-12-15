from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


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


def send_invitation_notification_email_to_sms(email):
    email_subject = "New invitation id request recieved"
    email_body = "Email: " + email
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "invitation@ekata.social",
        ["4344222257@txt.att.net"]
    )
    msg.send()


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


def send_csv_member_invitation_email(email, username, password, invitation_id):
    try:
        user = User.objects.get(username=username)
        gc_name = user.first_name if user.first_name else ''
    except ObjectDoesNotExist:
        gc_name = ''
    c = {
        'email': email,
        'invitation_id': invitation_id,
        'username': username,
        'password': password,
        'gc_name': gc_name
    }
    email_subject = "You are invited to Ekata"
    email_body = "Invitation id: " + invitation_id + "\nUsername: " + username + '\nPassword: ' + password
    email_html = render_to_string(
        'invitationsystem/csvinvitationemail.html',
        c
    )
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "invitation@ekata.social",
        [email]
    )
    msg.attach_alternative(email_html, "text/html")

    return msg.send(fail_silently=True)
