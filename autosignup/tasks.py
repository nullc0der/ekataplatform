from celery import shared_task
from autosignup.utils import send_email_verification_code,\
    send_phone_verfication_code, send_approval_mail, add_member_from_csv,\
    location_finder_util


@shared_task
def task_send_email_verfication_code(email, code):
    return send_email_verification_code(email, code)


@shared_task
def task_send_phone_verfication_code(phone, code):
    return send_phone_verfication_code(phone, code)


@shared_task
def task_send_approval_mail(signup, template_path=None):
    return send_approval_mail(signup, template_path)


@shared_task
def task_add_member_from_csv(accountprovidercsv, fetch_twilio=False):
    return add_member_from_csv(accountprovidercsv, fetch_twilio)


@shared_task
def task_find_location_and_save(address):
    return location_finder_util(address)
