import markdown
import csv
from bs4 import BeautifulSoup

from django.db import models
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from sysadmin.models import EmailUpdate, SystemUpdate, EmailGroup, EmailId

# Register your models here.


class EmailIdsInline(admin.TabularInline):
    model = EmailId


class EmailGroupAdmin(DjangoObjectActions, admin.ModelAdmin):
    inlines = [EmailIdsInline]

    actions = ['save_emailids_from_csv']
    change_actions = ['save_emailids_from_csv']

    @takes_instance_or_queryset
    def save_emailids_from_csv(self, request, queryset):
        count = 0
        for emailgroup in queryset:
            if emailgroup.csv_file:
                csv_f = open(emailgroup.csv_file.path, 'r')
                email_infos = csv.reader(csv_f)
                for email_info in email_infos:
                    emailid, created = EmailId.objects.get_or_create(
                        emailgroup=emailgroup,
                        first_name=email_info[0],
                        last_name=email_info[1],
                        email_id=email_info[2]
                    )
                    emailid.save()
                csv_f.close()
                count += 1
        self.message_user(request, '%s csvs data copied to emailgroup' % count)
    save_emailids_from_csv.short_description = 'Copy CSV data'
    save_emailids_from_csv.label = 'Copy CSV data'


class EmailUpdateAdmin(DjangoObjectActions, admin.ModelAdmin):
    actions = ['send_email_update']
    change_actions = ['send_email_update']

    @takes_instance_or_queryset
    def send_email_update(self, request, queryset):
        count = 0
        for emailupdate in queryset:
            groups = emailupdate.to_groups.all()
            subject = emailupdate.subject
            from_email = emailupdate.from_email
            email_html = emailupdate.message
            soup = BeautifulSoup(email_html)
            if soup.webversion:
                url = reverse('eblast', args=[emailupdate.id, ])
                url = "https://" + Site.objects.get_current().domain + url
                soup.webversion.clear()
                linktag = soup.new_tag('a', href=url)
                linktag.string = 'View email in browser'
                soup.webversion.append(linktag)
                email_html = soup.prettify()
            emailaddress_set = set()
            for group in groups:
                emailids = group.emailids.all()
                for emailid in emailids:
                    if emailid.email_id:
                        emailaddress_set.add(emailid.email_id.strip())
            for emailaddress in emailaddress_set:
                msg = EmailMultiAlternatives(
                    subject,
                    email_html,
                    from_email,
                    [emailaddress]
                )
                msg.attach_alternative(email_html, "text/html")
                msg.send()
            count += 1
            self.message_user(request, 'emailupdate %s sent' % emailupdate.id)
        self.message_user(request, "%s emailupdates sent successfully" % count)
    send_email_update.short_description = "Send eBlast"
    send_email_update.label = "Send eBlast"


admin.site.register(EmailUpdate, EmailUpdateAdmin)
admin.site.register(SystemUpdate)
admin.site.register(EmailGroup, EmailGroupAdmin)
