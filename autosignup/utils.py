import datetime
import re
import json
import requests
from iso3166 import countries

import piexif
import unicodecsv as csv

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import Template, Context
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.utils.timezone import now

from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException

from emailtosms.models import Carrier
from invitationsystem.models import Invitation
from profilesystem.models import UserAddress
from autosignup.models import CommunitySignup, GlobalEmail,\
    GlobalPhone, ReferralCode, AutoSignupAddress, AccountProvider
from groupsystem.models import BasicGroup, JoinRequest, GroupMemberRole,\
    GroupMemberExtraPerm
from groupsystem.views import MEMBER_PERMS


date_re = re.compile(
    r'(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{4})$'
)


def parse_date(value):
    match = date_re.match(value)
    if match:
        kw = {k: int(v) for k, v in six.iteritems(match.groupdict())}
        return datetime.date(**kw)


def add_user_to_group(user):
    accountprovider = AccountProvider.objects.get(name='grantcoin')
    basicgroup = accountprovider.basicgroup
    basicgroup.members.add(user)
    try:
        joinrequest = JoinRequest.objects.get(user=user, basic_group=basicgroup)
        joinrequest.approved = True
        joinrequest.save()
    except ObjectDoesNotExist:
        pass
    member_group = Group.objects.get(
        name='%s_member' % basicgroup.id
    )
    user.groups.add(member_group)
    groupmemberrole, created = GroupMemberRole.objects.get_or_create(
        basic_group=basicgroup,
        user=user
    )
    groupmemberrole.user = user
    groupmemberrole.role_name = 'member'
    groupmemberrole.save()
    extraperm = GroupMemberExtraPerm(basic_group=basicgroup)
    extraperm.user = user
    for perm in MEMBER_PERMS:
        setattr(extraperm, perm[0], True)
    extraperm.save()
    emailgroup = basicgroup.emailgroup
    emailgroup.users.add(user)


def unique_referral_code_generator():
    not_unique = True
    referral_code = ''
    while not_unique:
        code = get_random_string(
            length=10,
            allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789'
        )
        referral_codes = ReferralCode.objects.filter(code=code)
        if not len(referral_codes):
            not_unique = False
            referral_code = code
    return referral_code


def username_generator(full_name=None, first_name=None, last_name=None):
    needs_approval = False
    if full_name:
        s = full_name.split(' ')
        for i in range(len(s)):
            n = s[i].replace('-', '')
            s[i] = n
        string = ''.join(s).lower()
    elif first_name:
        if last_name:
            first_name = first_name.replace('-', '')
            last_name = last_name.replace('-', '')
            string = first_name.lower() + last_name.lower()
        else:
            last_name = last_name.replace('-', '')
            string = first_name.lower()
    else:
        string = get_random_string()
        needs_approval = True
    try:
        user = User.objects.get(username=string)
        return user
    except ObjectDoesNotExist:
        return (string, needs_approval)


def send_email_verification_code(email, code):
    c = {
        'code': code
    }
    email_subject = "Email Verification Code "
    email_body = "Code: " + code
    email_html = render_to_string('autosignup/email.html', c)
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "support@ekata.social",
        [email]
    )
    msg.attach_alternative(email_html, "text/html")

    return msg.send(fail_silently=False)


def send_phone_verfication_code(phone_no, code):
    account_sid = settings.EKATA_TWILIO_ACCOUNT_SID
    auth_token = settings.EKATA_TWILIO_AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(
        body='Use verification code: ' + code + '\nvalid for 30 min',
        to=phone_no,
        from_=settings.EKATA_TWILIO_PHONE_NO
    )
    return message.status


def collect_twilio_data(community_signup):
    lookup_url = 'https://lookups.twilio.com/v1/PhoneNumbers/' + \
        '%s?AddOns=whitepages_pro_caller_id' % community_signup.userphone
    res = requests.get(lookup_url, auth=(
        settings.EKATA_TWILIO_ACCOUNT_SID,
        settings.EKATA_TWILIO_AUTH_TOKEN
    ))
    if res.status_code == 200:
        data = json.loads(res.content)
        if data['add_ons']['results']['whitepages_pro_caller_id']['status'] == 'successful':
            try:
                name = data['add_ons']['results']['whitepages_pro_caller_id']['result']['results'][0]['belongs_to'][0]['names'][0]
                address = data['add_ons']['results']['whitepages_pro_caller_id']['result']['results'][0]['associated_locations'][0]
                country = countries.get(address['country_code'])
                twilio_address, created = AutoSignupAddress.objects.get_or_create(
                    address_type='twilio',
                    user=community_signup.user,
                    signup=community_signup,
                    zip_code=address['postal_code'] if address['postal_code'] else '',
                    city=address['city'] if address['city'] else '',
                    country=country.name
                )
                return twilio_address
            except:
                return False
        else:
            return False
    else:
        return False


def send_approval_mail(signup, template_path=None):
    try:
        referral_code = signup.user.referral_code.code
    except:
        referral_code = ""
    gc_name = signup.user.first_name if signup.user.first_name else signup.user.username
    c = {
        'gc_name': gc_name,
        'referral_code': referral_code
    }
    email_subject = "You have been approved a Grantcoin account."
    email_body = "Hello " + signup.user.username + ", Greetings from Ekata!!\n" + \
        "Grantcoin Foundation has approved your signup for a Grantcoin Account."
    if template_path:
        template_f = file(template_path, 'r')
        email_html = template_f.read()
        template = Template(email_html)
        context = Context({
            'gc_name': gc_name,
            'referral_code': referral_code
        })
        email_html = template.render(context)
        template_f.close()
    else:
        email_html = render_to_string('autosignup/email_approved.html', c)
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "grantcoin.signup@ekata.social",
        [signup.useremail]
    )
    msg.attach_alternative(email_html, "text/html")
    signup.approval_mail_sent = True
    signup.save()

    return msg.send(fail_silently=False)


class AddressCompareUtil(object):
    def __init__(self, from_city, to_city):
        self.from_city = from_city
        self.to_city = to_city

    def calculate_distance(self):
        from_add = self.from_city.latitude + ',' + self.from_city.longitude
        to_add = self.to_city.latitude + ',' + self.to_city.longitude
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=%s&destinations=%s" % (from_add, to_add)
        res = requests.get(url)
        distance = []
        data = json.loads(res.content)
        if data["rows"][0]["elements"][0]["status"] == "OK":
            distance.append(
                data["rows"][0]["elements"][0]["distance"]["text"]
            )
            distance.append(
                data["rows"][0]["elements"][0]["distance"]["value"]
            )
        return distance


def add_member_from_csv(accountprovidercsv, fetch_twilio=False):
    allowed_status = ['pending', 'approved', 'declined']
    if accountprovidercsv.csv:
        csv_file = open(accountprovidercsv.csv.path, 'r')
        membercsvs = csv.DictReader(csv_file)
        filename = '/tmp/%s.csv' % get_random_string()
        failed_csv_file = open(filename, 'w+')
        fieldnames = [
            'signup_date',
            'date_verified',
            'first_name',
            'last_name',
            'full_name',
            'house_number',
            'street',
            'zip_code',
            'city',
            'state',
            'country',
            'email_id',
            'phone_number',
            'referred_by',
            'referral_code',
            'wallet_address',
            'is_on_distribution',
            'status',
            'is_signed_up'
        ]
        failed_csv_writer = csv.DictWriter(failed_csv_file, fieldnames)
        failed_csv_writer.writeheader()
        integrate_status = ''
        processed_to = 0
        row_written = False
        c = 0
        for membercsv in membercsvs:
            try:
                twilio_data = ''
                invitation = None
                generated_username = username_generator(
                    membercsv['full_name'],
                    membercsv['first_name'],
                    membercsv['last_name']
                )
                while type(generated_username) is User:
                    no = get_random_string(length=4, allowed_chars='0123456789')
                    last_name = membercsv['last_name']
                    if membercsv['last_name']:
                        last_name = membercsv['last_name'] + str(no)
                    else:
                        last_name = str(no)
                    generated_username = username_generator(
                        first_name=membercsv['first_name'],
                        last_name=last_name
                    )
                username = generated_username[0]
                password = get_random_string(
                    length=5,
                    allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                )
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=membercsv['email_id'] if membercsv['email_id'] else None,
                    first_name=membercsv['first_name'] if membercsv['first_name'] else ' ',
                    last_name=membercsv['last_name'] if membercsv['last_name'] else ' ',
                )
                if user:
                    useraddress, created = UserAddress.objects.get_or_create(
                        user=user,
                        house_number=membercsv['house_number'],
                        street=membercsv['street'],
                        zip_code=membercsv['zip_code'],
                        city=membercsv['city'],
                        state=membercsv['state'],
                        country=membercsv['country']
                    )
                if membercsv['email_id']:
                    invitation, created = Invitation.objects.get_or_create(
                        email=membercsv['email_id'],
                        username=username,
                        password=password,
                        invitation_type='grantcoin'
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
                if fetch_twilio:
                    if membercsv['phone_number']:
                        signup.save()
                        twilio_data = collect_twilio_data(signup)
                signup.step_1_done = True
                signup.step_2_done = True
                signup.step_3_done = True
                signup.additional_step_done = True
                if membercsv['is_signed_up'].lower() == 'true':
                    if membercsv['status']:
                        if generated_username[1]:
                            signup.status = 'pending'
                            signup.auto_signup_fail_reason = 'Not enough data'
                        elif membercsv['status'].lower() in allowed_status:
                            signup.status = membercsv['status'].lower()
                            if membercsv['status'].lower() == 'approved':
                                referral_code = unique_referral_code_generator()
                                ReferralCode.objects.get_or_create(
                                    user=user,
                                    code=referral_code
                                )
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
                if invitation:
                    signup.invitation = invitation
                signup.data_collect_done = True  # Test: Upload a csv
                signup.save()
                add_user_to_group(signup.user)
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
                c += 1
                integrate_status = 'partially processed'
                processed_to = c
            except:
                failed_csv_writer.writerow(membercsv)
                row_written = True
        if row_written:
            accountprovidercsv.status = 'partially processed'
            accountprovidercsv.processed_to = processed_to
            failed_csv_file.close()
            with open(filename, 'rb') as doc_file:
                accountprovidercsv.failed_csv.save(filename, File(doc_file), save=True)
                accountprovidercsv.save()
        else:
            accountprovidercsv.status = 'processed'
            accountprovidercsv.processed_to = 'all'
        csv_file.close()
        accountprovidercsv.save()
    return c


def image_gps_metadata(image):
    try:
        exif_dict = piexif.load(image)
        gps = exif_dict['GPS']
        latref = gps[1]
        lat = gps[2]
        lonref = gps[3]
        lon = gps[4]
        latitude = float(lat[0][0]/lat[0][1]) + float(lat[1][0]/lat[1][1])/60\
            + float(lat[2][0]/lat[2][1])/3600
        longitude = float(lon[0][0]/lon[0][1]) + float(lon[1][0]/lon[1][1])/60\
            + float(lon[2][0]/lat[2][1])/3600
        if latref == 'S':
            latitude = -latitude
        if lonref == 'W':
            longitude = -longitude
        return "Latitude: %s Longitude: %s" % (latitude, longitude)
    except:
        return "No EXIF data found"


def location_finder_util(address):
    if address.zip_code:
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" % address.zip_code
    else:
        if address.city and address.country:
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" % (address.city + ',' + address.country)
        else:
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" % address.city
    if url:
        res = requests.get(url)
        data = json.loads(res.content)
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            address.latitude = location['lat']
            address.longitude = location['lng']
            address.save()


def remove_expired_referral_codes():
    removed = 0
    for code in ReferralCode.objects.all():
        if now() > code.added_on + datetime.timedelta(days=365) and not code.expired:
            code.expired = True
            code.save()
            removed += 1
    return removed


def calculate_referral_and_referrers():
    referrals = set()
    referrers = {}
    for i in User.objects.all():
        if hasattr(i, 'profile'):
            if i.profile.referred_by:
                referrer = i.profile.referred_by
                if referrer in referrers:
                    referrers[referrer] += 1
                else:
                    referrers[referrer] = 1
                referrals.add(i)
    return referrers, referrals
