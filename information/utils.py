from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_contact_email(email, first, last, company, telephone, comment):
    c = {
        'first': first,
        'last': last,
        'company': company,
        'email': email,
        'telephone': telephone,
        'comment': comment
    }
    email_subject = "New contact request recieved"
    email_body = "Firstname: " + first + '\nLastname: ' + last + '\nCompany: ' + company + '\nEmail Address: ' + email + '\nTelephone: ' + telephone + '\nComment: ' + comment
    email_html = render_to_string('information/email.html', c)
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "backend@ekata.social",
        ["support@basicincomeproject.org"]
    )
    msg.attach_alternative(email_html, "text/html")

    return msg.send()
