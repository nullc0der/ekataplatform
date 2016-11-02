from django.contrib import admin
from invitationsystem.models import Invitation

# Register your models here.


class InvitationAdmin(admin.ModelAdmin):
    list_filter = ('approved', )

admin.site.register(Invitation, InvitationAdmin)
