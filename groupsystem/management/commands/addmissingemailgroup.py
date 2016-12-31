from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from eblast.models import EmailGroup
from groupsystem.models import BasicGroup


class Command(BaseCommand):
    help = "Add missing emailgroup for groups"

    def handle(self, *args, **options):
        c = 0
        basicgroups = BasicGroup.objects.all()
        for basicgroup in basicgroups:
            try:
                emailgroup = basicgroup.emailgroup
            except ObjectDoesNotExist:
                emailgroup, created = EmailGroup.objects.get_or_create(
                    name=basicgroup.name,
                    basic_group=basicgroup
                )
                for user in basicgroup.super_admins.all():
                    emailgroup.users.add(user)
                for user in basicgroup.admins.all():
                    emailgroup.users.add(user)
                for user in basicgroup.moderators.all():
                    emailgroup.users.add(user)
                for user in basicgroup.members.all():
                    emailgroup.users.add(user)
                self.stdout.write(self.style.SUCCESS(
                    'Added emailgroup for group: "%s"' % basicgroup.name
                ))
                c += 1
        self.stdout.write(self.style.SUCCESS(
            'Successfully added "%s" emailgroup' % c
        ))
