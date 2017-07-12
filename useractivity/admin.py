from django.contrib import admin
from useractivity.models import FlaggedAccount

# Register your models here.


class FlaggedAccountAdmin(admin.ModelAdmin):
    readonly_fields = [
        'first_notice_sent_on',
        'second_notice_sent_on',
        'third_notice_sent_on'
    ]
    search_fields = ['user__username']
    list_filter = ('user_inactive', )


admin.site.register(FlaggedAccount, FlaggedAccountAdmin)
