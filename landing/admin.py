from django.contrib import admin

from markdownx.widgets import AdminMarkdownxWidget
from markdownx.models import MarkdownxField

from landing.models import News, Tags, HashtagImg, OgTag, NewsOgTag


# Register your models here.
class NewsOgTagInline(admin.StackedInline):
    model = NewsOgTag


class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsOgTagInline, ]
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }

admin.site.register(News, NewsAdmin)
admin.site.register(Tags)
admin.site.register(HashtagImg)
admin.site.register(OgTag)
