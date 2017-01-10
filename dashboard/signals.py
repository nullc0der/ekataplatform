from django.utils.timezone import now
from django.dispatch import receiver
from django.contrib.auth.models import User

from allauth.account.signals import user_signed_up
from dashboard.models import ActiveMemberCount, NewMemberCount,\
    TotalMemberCount


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
