import sys
from django.core.management.base import BaseCommand, CommandError

from autosignup.models import CommunitySignup, ReferralCode
from autosignup.utils import unique_referral_code_generator
from autosignup.tasks import task_send_approval_mail
from autosignup.views import get_selected_template_path


class Command(BaseCommand):
    help_text = 'Add referral_code for the users whose code is missing'

    def handle(self, *args, **options):
        c = 0
        missing_code_objs = ReferralCode.objects.filter(code='')
        confirmation = raw_input(
            "There are {} missing code, proceed(y/n)".format(
                len(missing_code_objs)))
        if confirmation == 'y':
            for i in missing_code_objs:
                referral_code = unique_referral_code_generator()
                i.code = referral_code
                i.save()
                signup = i.user.communitysignups.all()[0]
                if not signup.approval_mail_sent:
                    template_path = get_selected_template_path()
                    task_send_approval_mail.delay(signup, template_path)
                self.stdout.write(self.style.SUCCESS(
                    "{0} referral code set, code: {1}".format(i.user.username, i.code)
                ))
                c += 1
        else:
            sys.exit()
        self.stdout.write(self.style.SUCCESS(
            'Total referral code set: {0}'.format(c)
        ))
