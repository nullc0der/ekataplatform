from celery import shared_task
from invitationsystem.utils import \
    send_invitation_notification_email, send_invitation_email,\
    send_invitation_notification_email_to_sms, send_csv_member_invitation_email


@shared_task
def send_notification_to_reviewer(email):
    return send_invitation_notification_email(email)


@shared_task
def send_invitation(email, invitation_id):
    return send_invitation_email(email, invitation_id)


@shared_task
def task_send_notification_email_to_sms(email):
    return send_invitation_notification_email_to_sms(email)


@shared_task
def task_send_csv_member_invitation_email(
    email, username, password, invitation_id
):
    return send_csv_member_invitation_email(
        email, username, password, invitation_id
    )
