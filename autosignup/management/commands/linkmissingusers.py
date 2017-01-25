import unicodecsv as csv

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from autosignup.models import CommunitySignup, ReferralCode,\
 AutoSignupAddress, GlobalEmail, GlobalPhone
from autosignup.utils import unique_referral_code_generator
from profilesystem.models import UserAddress


class Command(BaseCommand):
    help_text = 'link community signup to users'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        allowed_status = ['pending', 'approved', 'declined']
        filename = options['filename']
        f = open(filename[0], 'r')
        membercsvs = csv.DictReader(f)
        row_number = 1
        success = 0
        for membercsv in membercsvs:
            self.stdout.write(self.style.SUCCESS(
                'Processing row: %s' % row_number
            ))
            user = User.objects.filter(email=membercsv['email_id'])[0]
            self.stdout.write(self.style.SUCCESS(
                'User: %s' % user.username
            ))
            useraddress, created = UserAddress.objects.get_or_create(
                user=user,
                house_number=membercsv['house_number'],
                street=membercsv['street'],
                zip_code=membercsv['zip_code'],
                city=membercsv['city'],
                state=membercsv['state'],
                country=membercsv['country']
            )
            signup, created = CommunitySignup.objects.get_or_create(
                user=user,
                community='grantcoin'
            )
            if user.address:
                asignupaddress, created = AutoSignupAddress.objects.get_or_create(
                    address_type='db',
                    user=user,
                    signup=signup,
                    house_number=user.address.house_number,
                    street=user.address.street,
                    zip_code=user.address.zip_code,
                    city=user.address.city,
                    state=user.address.state,
                    country=user.address.country
                )
            if membercsv['email_id']:
                signup.useremail = membercsv['email_id']
            if membercsv['phone_number']:
                signup.userphone = membercsv['phone_number']
            signup.step_1_done = True
            signup.step_2_done = True
            signup.step_3_done = True
            signup.additional_step_done = True
            if membercsv['is_signed_up'].lower() == 'true':
                if membercsv['status']:
                    if membercsv['status'].lower() in allowed_status:
                        signup.status = membercsv['status'].lower()
                    else:
                        signup.status = 'pending'
                        signup.auto_signup_fail_reason = 'Not a valid status'
                else:
                    signup.status = 'pending'
                    signup.auto_signup_fail_reason = 'Status field empty'
            else:
                signup.status = 'pending'
                signup.auto_signup_fail_reason = 'is_signed_up field is empty or false'
            signup.sent_to_community_staff = True
            if membercsv['signup_date']:
                signup.signup_date = parse_date(membercsv['signup_date'])
            if membercsv['date_verified']:
                signup.verified_date = parse_date(membercsv['date_verified'])
            if membercsv['wallet_address']:
                signup.wallet_address = membercsv['wallet_address']
            if membercsv['is_on_distribution']:
                signup.is_on_distribution = True
            signup.save()
            if membercsv['referral_code']:
                rcodes = ReferralCode.objects.filter(code=membercsv['referral_code'])
                if rcodes:
                    referral_code = unique_referral_code_generator()
                    rcode_obj, created = ReferralCode.objects.get_or_create(
                        user=signup.user
                    )
                    rcode_obj.code = referral_code
                    rcode_obj.save()
                    audit_file_path = settings.BASE_DIR + '/static/dist/files/audit.log'
                    datetime = now().strftime("%Y-%m-%d %H:%I")
                    line = "\n" + datetime + ": Referral code for user " + \
                        signup.user.username + " changed from " + \
                        membercsv['referral_code'] + " to " + referral_code
                    f = open(audit_file_path, 'a+')
                    f.write(line)
                    f.close()
                else:
                    rcode_obj, created = ReferralCode.objects.get_or_create(
                        user=signup.user
                    )
                    rcode_obj.code = membercsv['referral_code']
                    rcode_obj.save()
                if membercsv['referred_by']:
                    try:
                        rcode_obj = ReferralCode.objects.get(
                            code=membercsv['referred_by']
                        )
                        signup.user.profile.referred_by = rcode_obj.user
                        signup.user.profile.save()
                    except ObjectDoesNotExist:
                        pass
            else:
                referral_code = unique_referral_code_generator()
                rcode_obj, created = ReferralCode.objects.get_or_create(
                    user=signup.user
                )
                rcode_obj.code = referral_code
                rcode_obj.save()
            try:
                globalphone = GlobalPhone.objects.get(
                    phone=signup.userphone
                )
                globalphone.signup.add(signup)
            except ObjectDoesNotExist:
                globalphone, created = GlobalPhone.objects.get_or_create(
                    phone=signup.userphone
                )
                globalphone.signup.add(signup)
            try:
                globalemail = GlobalEmail.objects.get(
                    email=signup.useremail
                )
                globalemail.signup.add(signup)
            except ObjectDoesNotExist:
                globalemail, created = GlobalEmail.objects.get_or_create(
                    email=signup.useremail
                )
                globalemail.signup.add(signup)
            row_number += 1
            success += 1
            self.stdout.write(self.style.SUCCESS(
                'Successfully linked user: %s to signup: %s' % (user.username, signup.id)
            ))
        f.close()
        self.stdout.write(self.style.SUCCESS(
            'Successfully linked: %s users' % success
        ))
