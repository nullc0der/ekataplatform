from django.contrib import admin

from autosignup.models import CommunitySignup, EmailVerfication
# Register your models here.

admin.site.register(CommunitySignup)
admin.site.register(EmailVerfication)
