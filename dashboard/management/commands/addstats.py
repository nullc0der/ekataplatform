from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from dashboard.models import ActiveMemberCount, NewMemberCount,\
 TotalMemberCount


class Command(BaseCommand):
    help_text = 'Add user stats to widgets'

    def handle(self, *args, **options):
        totalmembers = 0
        for user in User.objects.all():
            newmember, created = NewMemberCount.objects.get_or_create(
                date=user.date_joined.date()
            )
            newmember.count += 1
            newmember.save()
            if user.last_login:
                activemember, created = ActiveMemberCount.objects.get_or_create(
                    date=user.last_login.date()
                )
                activemember.users.add(user)
        for newmember in NewMemberCount.objects.order_by('date'):
            totalmembers += newmember.count
            totalmember, created = TotalMemberCount.objects.get_or_create(
                date=newmember.date
            )
            totalmember.count = totalmembers
            totalmember.save()
        self.stdout.write(self.style.SUCCESS(
            'Successfully created stats'
        ))
