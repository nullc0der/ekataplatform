from django.core.mail import EmailMultiAlternatives


def send_carrier_code_email(email, phone_number, code):
    email_subject = "Ekata Carrier Verification"
    email_body = "Code: " + code
    email_splited = email.split('@')
    new_email = str(phone_number) + '@' + email_splited[1]
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "support@ekata.social",
        [new_email]
    )
    msg.send()
