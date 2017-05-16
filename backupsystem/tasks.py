from celery.task import periodic_task
from celery.schedules import crontab

from backupsystem.utils import create_backup


@periodic_task(run_every=crontab(minute=0, hour=0))
def task_create_backup(manual=False):
    return create_backup(manual=False)
