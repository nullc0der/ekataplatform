from celery import shared_task
from profilesystem.utils import unique_ekata_id_setter


@shared_task
def task_unique_ekata_id_setter(sender, profile):
    return unique_ekata_id_setter(sender, profile)
