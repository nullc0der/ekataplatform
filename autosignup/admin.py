from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from autosignup.models import CommunitySignup, AccountAddContact, AccountProvider
# Register your models here.

admin.site.register(CommunitySignup, SimpleHistoryAdmin)
admin.site.register(AccountAddContact)
admin.site.register(AccountProvider)
