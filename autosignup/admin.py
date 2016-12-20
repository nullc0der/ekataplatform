from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from autosignup.models import CommunitySignup, AccountAddContact, AccountProvider
# Register your models here.


class CommunitySignupAdmin(SimpleHistoryAdmin):
    search_fields = ['user__username']


admin.site.register(CommunitySignup, CommunitySignupAdmin)
admin.site.register(AccountAddContact)
admin.site.register(AccountProvider)
