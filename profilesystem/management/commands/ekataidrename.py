from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help_text = 'Change not logged in ekata_id to registered'

    def handle(self, *args, **options):
        c = 0
        for user in User.objects.all():
            if not user.last_login:
                if hasattr(user, 'profile'):
                    ekata_id = user.profile.ekata_id.split('.')
                    if len(ekata_id) > 2:
                        if ekata_id[2] == 'member':
                            ekata_id[2] = 'registered'
                            user.profile.ekata_id = '.'.join(ekata_id)
                            user.profile.save()
                            self.stdout.write(self.style.SUCCESS(
                                "user %s's id changed to %s " % (user.username, user.profile.ekata_id)
                            ))
                            c += 1
        self.stdout.write(self.style.SUCCESS(
            'Successfully changed id for : %s users' % c
        ))
