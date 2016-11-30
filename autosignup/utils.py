import json
import requests
from iso3166 import countries

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache

from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException

from emailtosms.models import Carrier


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
        s = ""
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
        return t + ',' + s

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
