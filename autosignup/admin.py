from django.contrib import admin

from autosignup.models import CommunitySignup, EmailVerfication, PhoneVerification
# Register your models here.

admin.site.register(CommunitySignup)
admin.site.register(EmailVerfication)
admin.site.register(PhoneVerification)
