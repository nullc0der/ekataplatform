from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from autosignup.models import CommunitySignup, AccountAddContact, AccountProvider, PhoneVerification
# Register your models here.

admin.site.register(CommunitySignup, SimpleHistoryAdmin)
admin.site.register(AccountAddContact)
admin.site.register(AccountProvider)
admin.site.register(PhoneVerification)
