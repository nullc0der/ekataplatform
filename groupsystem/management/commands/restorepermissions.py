from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm
from groupsystem.models import BasicGroup
from groupsystem.views import SUBSCRIBER_PERMS, MEMBER_PERMS,\
    MODERATOR_PERMS, ADMIN_PERMS, SUPERADMIN_PERMS


class Command(BaseCommand):
    help_text = 'Restore permission to BasicGroups permission Group'

    def handle(self, *args, **kwargs):
        for basicgroup in BasicGroup.objects.all():
            super_admin_group = Group.objects.get(
                name='%s_superadmin' % basicgroup.id
            )
            admin_group = Group.objects.get(
                name='%s_admin' % basicgroup.id
            )
            moderator_group = Group.objects.get(
                name='%s_moderator' % basicgroup.id
            )
            member_group = Group.objects.get(
                name='%s_member' % basicgroup.id
            )
            subscriber_group = Group.objects.get(
                name='%s_subscriber' % basicgroup.id
            )
            for perm in SUPERADMIN_PERMS:
                assign_perm(perm[0], super_admin_group, basicgroup)
            for perm in ADMIN_PERMS:
                assign_perm(perm[0], admin_group, basicgroup)
            for perm in MODERATOR_PERMS:
                assign_perm(perm[0], moderator_group, basicgroup)
            for perm in MEMBER_PERMS:
                assign_perm(perm[0], member_group, basicgroup)
            for perm in SUBSCRIBER_PERMS:
                assign_perm(perm[0], subscriber_group, basicgroup)
        self.stdout.write(
            self.style.SUCCESS("Done")
        )
