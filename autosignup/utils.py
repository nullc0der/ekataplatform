import json
import requests
from iso3166 import countries
import csv

import piexif

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist

from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException

from emailtosms.models import Carrier
from invitationsystem.models import Invitation
from profilesystem.models import UserAddress
from autosignup.models import CommunitySignup, GlobalEmail, GlobalPhone


def username_generator(full_name=None, first_name=None, last_name=None):
    needs_approval = False
    if full_name:
        string = full_name
    elif first_name:
        if last_name:
            string = first_name + last_name
        else:
            string = first_name
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
    lookup = cache.get('%s_lookup' % phone_no)
    if lookup:
        carrier_name = lookup['carrier']['name']
        carrier = Carrier.objects.filter(
            name__iexact=carrier_name.lower(),
            verified=True
        )
        if carrier:
            email_subject = "Verification code"
            email_body = "Code: " + code + '\nvalid for 30 min'
            email_splited = carrier[0].email.split('@')
            new_email = str(phone_number) + '@' + email_splited[1]
            msg = EmailMultiAlternatives(
                email_subject,
                email_body,
                "support@ekata.social",
                [new_email]
            )
            return msg.send()
        else:
            account_sid = settings.EKATA_TWILIO_ACCOUNT_SID
            auth_token = settings.EKATA_TWILIO_AUTH_TOKEN
            client = TwilioRestClient(account_sid, auth_token)
            message = client.messages.create(
                body='Use verification code: ' + code + '\nvalid for 30 min',
                to=phone_no,
                from_=settings.EKATA_TWILIO_PHONE_NO
            )
            return message.status
    else:
        account_sid = settings.EKATA_TWILIO_ACCOUNT_SID
        auth_token = settings.EKATA_TWILIO_AUTH_TOKEN
        client = TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(
            body='Use verification code: ' + code + '\nvalid for 30 min',
            to=phone_no,
            from_=settings.EKATA_TWILIO_PHONE_NO
        )
        return message.status


def collect_twilio_data(phone_no):
    lookup_url = 'https://lookups.twilio.com/v1/PhoneNumbers/' + \
        '%s?AddOns=whitepages_pro_caller_id' % phone_no
    res = requests.get(lookup_url, auth=(
        settings.EKATA_TWILIO_ACCOUNT_SID,
        settings.EKATA_TWILIO_AUTH_TOKEN
    ))
    if res.status_code == 200:
        data = json.loads(res.content)
        if data['add_ons']['results']['whitepages_pro_caller_id']['status'] == 'successful':
            name = data['add_ons']['results']['whitepages_pro_caller_id']['result']['results'][0]['belongs_to'][0]['names'][0]
            address = data['add_ons']['results']['whitepages_pro_caller_id']['result']['results'][0]['associated_locations'][0]
            country = countries.get(address['country_code'])
            twilio_address = 'first_name: %s ; \nlast_name: %s ; \ncity: %s ; \ncountry: %s ; \nzip_code: %s ; \n' %\
                (name['first_name'], name['last_name'], address['city'], country.name, address['postal_code'])
            return twilio_address
        else:
            return False
    else:
        return False


def send_approval_mail(signup, template_path=None):
    c = {
        'username': signup.user.username,
    }
    email_subject = "You are approved for Grantcoin Account "
    email_body = "Hello " + signup.user.username + "Greetings from Ekata!!\n" + \
        "Grantcoin approved your signup for their account"
    if template_path:
        template = file(template_path, 'r')
        email_html = template.read()
        template.close()
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

    def _extract_city(self, city, twilio=False):
        t = ""
        """
        for d in city:
            v = d.strip()
            if v.startswith('city:'):
                t = v.split(':')[1]
            if not twilio:
                if v.startswith('state:'):
                    s = v.split(':')[1]
            else:
                if v.startswith('country:'):
                    s = v.split(':')[1]
        """
        for d in city:
            v = d.strip()
            if v.startswith('zip_code:'):
                t = v.split(':')[1]
        return t

    def calculate_distance(self):
        from_add = self._extract_city(self.from_city)
        to_add = self._extract_city(self.to_city, twilio=True)
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=%s&destinations=%s" % (from_add, to_add)
        res = requests.get(url)
        if res.status_code == 200:
            data = json.loads(res.content)
            if data["rows"][0]["elements"][0]["status"] == "OK":
                distance = []
                distance.append(
                    data["rows"][0]["elements"][0]["distance"]["text"]
                )
                distance.append(
                    data["rows"][0]["elements"][0]["distance"]["value"]
                )
            else:
                distance = []
        return distance


def send_csv_member_invitation_email(email, username, password, invitation_id):
    c = {
        'email': email,
        'invitation_id': invitation_id,
        'username': username,
        'password': password
    }
    email_subject = "You are invited to Ekata"
    email_body = "Invitation id: " + invitation_id + "\nUsername: " + username + '\nPassword: ' + password
    email_html = render_to_string(
        'invitationsystem/csvinvitationemail.html',
        c
    )
    msg = EmailMultiAlternatives(
        email_subject,
        email_body,
        "invitation@ekata.social",
        [email]
    )
    msg.attach_alternative(email_html, "text/html")

    msg.send(fail_silently=True)


def add_member_from_csv(accountprovidercsv, fetch_twilio=False):
    allowed_status = ['pending', 'approved', 'declined']
    if accountprovidercsv.csv:
        csv_file = open(accountprovidercsv.csv.path, 'r')
        membercsvs = csv.DictReader(csv_file)
        for membercsv in membercsvs:
            c = 0
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
                first_name=membercsv['first_name'] if membercsv['first_name'] else None,
                last_name=membercsv['last_name'] if membercsv['last_name'] else None,
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
                if membercsv['is_signed_up'].lower() == 'true':
                    invitation, created = Invitation.objects.get_or_create(
                        email=membercsv['email_id'],
                        username=username,
                        password=password,
                        invitation_type='grantcoin'
                    )
                else:
                    invitation, created = Invitation.objects.get_or_create(
                        email=membercsv['email_id'],
                        username=username,
                        password=password,
                        sent=True,
                        invitation_type='grantcoin'
                    )
                    send_csv_member_invitation_email(
                        email=invitation.email,
                        invitation_id=invitation.invitation_id,
                        username=invitation.username,
                        password=invitation.password
                    )
            if fetch_twilio:
                if membercsv['phone_number']:
                    twilio_data = collect_twilio_data(membercsv['phone_number'])
            if membercsv['is_signed_up'].lower() == 'true':
                signup, created = CommunitySignup.objects.get_or_create(
                    user=user,
                    community='grantcoin'
                )
                if user.address:
                    useraddress_in_db = 'house_number: ' + user.address.house_number + '; \n street: ' + user.address.street +\
                        '; \n city: ' + user.address.city + '; \n state: ' + user.address.state + '; \n country: ' + user.address.country
                    signup.useraddress_in_db = useraddress_in_db
                if membercsv['email_id']:
                    signup.useremail = membercsv['email_id']
                if membercsv['phone_number']:
                    signup.userphone = membercsv['phone_number']
                if twilio_data:
                    signup.useraddress_from_twilio = twilio_data
                signup.step_1_done = True
                signup.step_2_done = True
                signup.step_3_done = True
                signup.additional_step_done = True
                if membercsv['status']:
                    if generated_username[1]:
                        signup.status = 'pending'
                    elif membercsv['status'].lower() in allowed_status:
                        signup.status = membercsv['status'].lower()
                    else:
                        signup.status = 'pending'
                signup.sent_to_community_staff = True
                if membercsv['signup_date']:
                    signup.signup_date = parse_date(membercsv['signup_date'])
                if membercsv['date_verified']:
                    signup.verified_date = parse_date(membercsv['date_verified'])
                if membercsv['referred_by']:
                    signup.referred_by = membercsv['referred_by']
                if membercsv['referral_code']:
                    signup.referral_code = membercsv['referral_code']
                if membercsv['wallet_address']:
                    signup.wallet_address = membercsv['wallet_address']
                if membercsv['is_on_distribution']:
                    signup.is_on_distribution = True
                if invitation:
                    signup.invitation = invitation
                signup.save()
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
            accountprovidercsv.status = 'partially processed'
            accountprovidercsv.processed_to = c
            accountprovidercsv.save()
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
