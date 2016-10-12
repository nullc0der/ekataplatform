import markdown

from celery.decorators import periodic_task
from celery.schedules import crontab

from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from sysadmin.models import EmailUpdate


@periodic_task(
    run_every=(crontab()),
    name="task_send_update_email",
)
def send_update_email_to_users():
    emailupdates = EmailUpdate.objects.all()
    for emailupdate in emailupdates:
        if not emailupdate.sent:
            if timezone.now() > emailupdate.timestamp:
                users = emailupdate.to_users.all()
                subject = emailupdate.subject
                from_email = emailupdate.from_email
                message = emailupdate.message
                email_html = markdown.markdown(message)
                emailaddress_list = []
                for user in users:
                    if user.email:
                        emailaddress_list.append(user.email)
                for emailaddress in emailaddress_list:
                    msg = EmailMultiAlternatives(
                        subject,
                        email_html,
                        from_email,
                        [emailaddress]
                    )
                    msg.attach_alternative(email_html, "text/html")
                    msg.send()
                emailupdate.sent = True
                emailupdate.save()
