from celery.schedules import crontab
from celery.decorators import periodic_task

from dashboard.utils import set_total_members


@periodic_task(
    run_every=crontab(minute=0, hour=0)
)
def task_set_total_members():
    return set_total_members()
