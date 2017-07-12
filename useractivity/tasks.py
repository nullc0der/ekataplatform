from celery.task import periodic_task
from celery.schedules import crontab

from useractivity.utils import check_users, check_flagged_accounts


@periodic_task(run_every=crontab(minute=0, hour=0))
def task_check_users():
    return check_users()


@periodic_task(run_every=crontab(minute=0, hour=0))
def task_check_flagged_accounts():
    return check_flagged_accounts()
