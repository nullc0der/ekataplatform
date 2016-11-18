from celery import shared_task
from autosignup.utils import send_email_verification_code,\
    send_phone_verfication_code


@shared_task
def task_send_email_verfication_code(email, code):
    return send_email_verification_code(email, code)


@shared_task
def task_send_phone_verfication_code(phone, code):
    return send_phone_verfication_code(phone, code)
