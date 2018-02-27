from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
from groupsystem.utils import (
    create_emailgroup,
    send_serialized_user, create_notification,
    process_flagged_for_delete_group)


@shared_task
def task_create_emailgroup(basicgroup):
    return create_emailgroup(basicgroup)


@shared_task
def task_send_serialized_user(pk_set):
    return send_serialized_user(pk_set)


@shared_task
def task_create_notification(obj, basicgroup):
    return create_notification(obj, basicgroup)


@periodic_task(run_every=crontab(minute=0, hour=12))
def task_process_flagged_for_delete_group():
    return process_flagged_for_delete_group()
