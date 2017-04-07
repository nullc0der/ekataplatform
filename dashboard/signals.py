from django.utils.timezone import now
from django.dispatch import receiver
from django.contrib.auth.models import User

from allauth.account.signals import user_signed_up, user_logged_in
from dashboard.models import ActiveMemberCount, NewMemberCount,\
    TotalMemberCount
from eblast.models import EmailGroup


@receiver(user_signed_up)
def add_new_and_total_member(request, user, **kwargs):
    newmember, created = NewMemberCount.objects.get_or_create(
        date=now().date()
    )
    newmember.count += 1
    newmember.save()
    totaluser = User.objects.count()
    totalmember, created = TotalMemberCount.objects.get_or_create(
        date=now().date()
    )
    totalmember.count = totaluser
    totalmember.save()


@receiver(user_logged_in)
def set_active_member(request, user, **kwargs):
    activemember, created = ActiveMemberCount.objects.get_or_create(
        date=now().date()
    )
    activemember.users.add(user)


@receiver(user_signed_up)
def add_member_to_emailgroup(request, user, **kwargs):
    emailgroup = EmailGroup.objects.filter(all_members_group=True)
    if len(emailgroup):
        emailgroup = emailgroup[0]
        emailgroup.users.add(user)
