from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from landing.models import News, Tags, HashtagImg


# Register your models here.
admin.site.register(News, MarkdownxModelAdmin)
admin.site.register(Tags)
admin.site.register(HashtagImg)
