from celery.schedules import crontab
from celery.decorators import periodic_task

from dashboard.utils import set_active_members


@periodic_task(
    run_every=crontab(minute='*/5')
)
def task_set_active_members():
    return set_active_members()
