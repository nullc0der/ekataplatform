from celery import shared_task
from groupsystem.utils import create_emailgroup, send_serialized_user


@shared_task
def task_create_emailgroup(basicgroup):
    return create_emailgroup(basicgroup)


@shared_task
def task_send_serialized_user(pk_set):
    return send_serialized_user(pk_set)
