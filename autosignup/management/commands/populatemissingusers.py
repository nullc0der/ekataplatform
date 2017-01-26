from django.core.management.base import BaseCommand, CommandError

from autosignup.models import CommunitySignup
from autosignup.utils import add_user_to_group


class Command(BaseCommand):
    help_text = 'add members to groups'

    def handle(self, *args, **options):
        c = 0
        for commmunitysignup in CommunitySignup.objects.all():
            if commmunitysignup.status == 'approved':
                add_user_to_group(commmunitysignup.user)
                c += 1
        self.stdout.write(self.style.SUCCESS(
            'Added: %s' % c
        ))
