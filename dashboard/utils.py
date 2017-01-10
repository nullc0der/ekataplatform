from django.utils.timezone import now
from django.contrib.auth.models import User

from dashboard.models import TotalMemberCount


def set_total_members():
    totaluser = User.objects.count()
    totalmember, created = TotalMemberCount.objects.get_or_create(
        date=now().date()
    )
    totalmember.count = totaluser
    totalmember.save()
