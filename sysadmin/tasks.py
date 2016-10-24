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
                groups = emailupdate.to_groups.all()
                subject = emailupdate.subject
                from_email = emailupdate.from_email
                message = emailupdate.message
                email_html = markdown.markdown(message)
                emailaddress_set = set()
                for group in groups:
                    for user in group.users.all():
                        if user.email:
                            emailaddress_set.add(user.email)
                for emailaddress in emailaddress_set:
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
