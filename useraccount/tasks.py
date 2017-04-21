from celery import shared_task
from useraccount.utils import send_distribute_phone_verfication, dist_ekata_units


@shared_task
def task_send_distribute_phone_verfication(phone_no, code):
    return send_distribute_phone_verfication(phone_no, code)


@shared_task
def task_dist_ekata_units(amount):
    return dist_ekata_units(amount)
