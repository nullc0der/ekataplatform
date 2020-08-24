from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from useractivity.models import FlaggedAccount


def create_flaggedaccount(user):
    try:
        flaggedaccount = FlaggedAccount.objects.get(user=user)
    except ObjectDoesNotExist:
        flaggedaccount = FlaggedAccount(user=user)
    if user.profile.avatar:
        flaggedaccount.has_avatar = True
    if user.communitysignups.all():
        flaggedaccount.has_gc_signup = True
    if hasattr(user, 'address'):
        flaggedaccount.has_address = True
    if user.get_full_name():
        flaggedaccount.has_name_fields = True
    if user.socialaccount_set.all():
        flaggedaccount.has_socials = True
    if user.connection_sender.all() or user.connection_reciever.all():
        flaggedaccount.has_connections = True
    if user.grouppost_set.all():
        flaggedaccount.has_posts = True
    if user.message_set.all():
        flaggedaccount.has_messages = True
    flaggedaccount.first_notice_sent_on = now()
    flaggedaccount.second_notice_sent_on = None
    flaggedaccount.third_notice_sent_on = None
    flaggedaccount.save()


def send_email(user, email_number):
    maximum_inactivity = 120
    if email_number == 1:
        subject = "Account Inactivity Notice"
        response_wait = 30
        html = render_to_string(
            'useractivity/emails/first_notice.html',
            context={
                'response_wait': response_wait,
                'maximum_inactivity': maximum_inactivity
            }
        )
    if email_number == 2:
        subject = "Account Action Required"
        response_wait = 3
        html = render_to_string(
            'useractivity/emails/second_notice.html',
            context={
                'response_wait': response_wait,
                'maximum_inactivity': maximum_inactivity
            }
        )
    if email_number == 3:
        subject = "Account Deactivated"
        html = render_to_string(
            'useractivity/emails/third_notice.html',
        )
    msg = EmailMultiAlternatives(
        subject,
        '',
        "support@ekata.social",
        [user.email]
    )
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=True)


def check_users():
    if settings.USERACTIVITY_SERVICE_ACTIVE:
        active_users = User.objects.filter(is_active=True)
        total_flagged_accounts = 0
        for user in active_users:
            if hasattr(user, 'communitysignups'):
                if not user.communitysignups.all():
                    if user.last_login:
                        if user.last_login + timedelta(days=120) <= now() and not hasattr(user, 'flaggedaccount'):
                            create_flaggedaccount(user)
                            send_email(user, 1)
                            total_flagged_accounts += 1
                    else:
                        if not hasattr(user, 'flaggedaccount'):
                            create_flaggedaccount(user)
                            send_email(user, 1)
                            total_flagged_accounts += 1
        return "Processed total flagged accounts %s" % total_flagged_accounts
    else:
        return "Service is not active"


def check_flagged_accounts():
    if settings.USERACTIVITY_SERVICE_ACTIVE:
        for flaggedaccount in FlaggedAccount.objects.all():
            if flaggedaccount.second_notice_sent_on:
                if flaggedaccount.second_notice_sent_on + timedelta(days=3) <= now() and not flaggedaccount.third_notice_sent_on:
                    send_email(flaggedaccount.user, 3)
                    flaggedaccount.third_notice_sent_on = now()
                    flaggedaccount.user_inactive = True
                    flaggedaccount.save()
            if flaggedaccount.first_notice_sent_on:
                if flaggedaccount.first_notice_sent_on + timedelta(days=27) <= now() and not flaggedaccount.second_notice_sent_on:
                    send_email(flaggedaccount.user, 2)
                    flaggedaccount.second_notice_sent_on = now()
                    flaggedaccount.save()
        return True
    else:
        return "Service is not active"
