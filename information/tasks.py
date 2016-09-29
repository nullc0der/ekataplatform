from celery import shared_task
from information.utils import send_contact_email


@shared_task
def send_contact_email_task(email, first, last, company, telephone, comment):
    return send_contact_email(email, first, last, company, telephone, comment)
