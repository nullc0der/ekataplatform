from celery import shared_task
from eblast.utils import send_test_mail, send_campaign_email


@shared_task
def task_send_test_mail(id, from_email, to_email):
    return send_test_mail(id, from_email, to_email)


@shared_task
def task_send_campaign_email(id, from_email, groups):
    return send_campaign_email(id, from_email, groups)
