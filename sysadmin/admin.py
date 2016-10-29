import markdown

from django.db import models
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives

from sysadmin.models import EmailUpdate, SystemUpdate, EmailGroup, EmailId

# Register your models here.


class EmailIdsInline(admin.TabularInline):
    model = EmailId


class EmailGroupAdmin(admin.ModelAdmin):
    inlines = [EmailIdsInline]


class EmailUpdateAdmin(admin.ModelAdmin):
    actions = ['send_email_update']

    def send_email_update(self, request, queryset):
        count = 0
        for emailupdate in queryset:
            groups = emailupdate.to_groups.all()
            subject = emailupdate.subject
            from_email = emailupdate.from_email
            email_html = emailupdate.message
            emailaddress_set = set()
            for group in groups:
                for user in group.users.all():
                    if user.email:
                        emailaddress_set.add(user.email.strip())
                other_emails = group.emailids.all()
                for other_email in other_emails:
                    if other_email.email_id:
                        emailaddress_set.add(other_email.email_id.strip())
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
        self.message_user(request, "%s emailupdates sent successfully" % count)
    send_email_update.short_description = "Send eBlast"


admin.site.register(EmailUpdate, EmailUpdateAdmin)
admin.site.register(SystemUpdate)
admin.site.register(EmailGroup, EmailGroupAdmin)
