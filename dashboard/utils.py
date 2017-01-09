from django.utils.timezone import now
from django.contrib.auth.models import User

from dashboard.models import ActiveMemberCount


def set_active_members():
    active = 0
    for user in User.objects.all():
        if hasattr(user, 'profile'):
            if user.profile.online():
                active += 1
    activemember, created = ActiveMemberCount.objects.get_or_create(
        date=now().date()
    )
    activemember.count = active
    activemember.save()
