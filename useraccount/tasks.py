from __future__ import absolute_import


from datetime import timedelta
from celery.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.utils import timezone
from useraccount.models import IncomeRelease, UserAccount
from usertimeline.models import UserTimeline
from notification.utils import create_notification

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab()),
    name="task_release_income",
)
def release_income():
    users = User.objects.all()
    now = timezone.now()
    for user in users:
        useraccount, created = UserAccount.objects.get_or_create(user=user)
        if now >= useraccount.next_release:
            release = IncomeRelease(user=user)
            release.amount = 1024
            useraccount.next_release += timedelta(minutes=4)
            useraccount.balance += 1024
            usertimeline = UserTimeline(user=user)
            usertimeline.amount = 1024
            usertimeline.timeline_type = 3
            useraccount.save()
            release.save()
            usertimeline.save()
            logger.info("released to %s", user.username)
            create_notification(
                user=user,
                ntype=3,
                amount=1024
            )
