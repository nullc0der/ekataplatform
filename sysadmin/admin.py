from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from sysadmin.models import EmailUpdate, SystemUpdate

# Register your models here.

admin.site.register(EmailUpdate, MarkdownxModelAdmin)
admin.site.register(SystemUpdate)
