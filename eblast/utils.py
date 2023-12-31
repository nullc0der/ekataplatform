from bs4 import BeautifulSoup

from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from eblast.models import EmailId, EmailCampaign, CampaignTracking


def send_test_mail(id, from_email, to_email):
    emailcampaign = EmailCampaign.objects.get(id=id)
    email_html = emailcampaign.message
    subject = emailcampaign.subject
    soup = BeautifulSoup(email_html)
    if soup.webversion:
        url = '/eblast/campaign/' + str(emailcampaign.id) + '/'
        url = "https://" + Site.objects.get_current().domain + url
        soup.webversion.clear()
        linktag = soup.new_tag('a', href=url)
        linktag.string = 'View in browser'
        soup.webversion.append(linktag)
        email_html = soup.prettify()
    usernames = User.objects.filter(email=to_email)
    email_html = Template(email_html)
    context = Context({'username': usernames[0] if usernames else emailaddress})
    email_html = email_html.render(context)
    msg = EmailMultiAlternatives(
        subject,
        email_html,
        from_email,
        [to_email]
    )
    msg.attach_alternative(email_html, "text/html")
    return msg.send()


def send_campaign_email(id, from_email, groups):
    emailaddress_set = set()
    for group in groups:
        emailids = group.emailids.all()
        for emailid in emailids:
            if emailid.email_id and emailid.send_email_from_group:
                emailaddress_set.add(emailid.email_id.strip())
    for emailaddress in emailaddress_set:
        emailcampaign = EmailCampaign.objects.get(id=id)
        email_html = emailcampaign.message
        subject = emailcampaign.subject
        soup = BeautifulSoup(email_html)
        if soup.webversion:
            url = '/eblast/campaign/' + str(emailcampaign.id) + '/'
            url = "https://" + Site.objects.get_current().domain + url
            soup.webversion.clear()
            linktag = soup.new_tag('a', href=url)
            linktag.string = 'View in browser'
            soup.webversion.append(linktag)
            email_html = soup.prettify()
        campaigntracking, created = CampaignTracking.objects.get_or_create(
            campaign=emailcampaign,
            emailid=emailaddress,
            sent=True
        )
        url = '/en/eblast/image/' + emailcampaign.tracking_id + '/' + campaigntracking.tracking_id + '/'
        url = "https://" + Site.objects.get_current().domain + url
        image_tag = '<img src="' + url + '" style="visibity: hidden"></img>'
        usernames = User.objects.filter(email=emailaddress)
        email_html = Template(email_html)
        context = Context({'image_tag': image_tag, 'username': usernames[0] if usernames else emailaddress})
        email_html = email_html.render(context)
        msg = EmailMultiAlternatives(
            subject,
            email_html,
            from_email,
            [emailaddress]
        )
        msg.attach_alternative(email_html, "text/html")
        msg.send()
