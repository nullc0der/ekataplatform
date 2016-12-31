from celery import shared_task
from groupsystem.utils import create_emailgroup


@shared_task
def task_create_emailgroup(basicgroup):
    return create_emailgroup(basicgroup)
