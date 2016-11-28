from celery import shared_task
from autosignup.utils import send_email_verification_code,\
    send_phone_verfication_code, send_approval_mail


@shared_task
def task_send_email_verfication_code(email, code):
    return send_email_verification_code(email, code)


@shared_task
def task_send_phone_verfication_code(phone, code):
    return send_phone_verfication_code(phone, code)


@shared_task
def task_send_approval_mail(signup, template_path=None):
    return send_approval_mail(signup, template_path)
