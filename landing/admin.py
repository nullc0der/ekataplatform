from django.contrib import admin

from markdownx.widgets import AdminMarkdownxWidget
from markdownx.models import MarkdownxField

from landing.models import\
    News, Tags, HashtagImg, OgTag, NewsOgTag, ExtraMetaTag


# Register your models here.
class NewsOgTagInline(admin.StackedInline):
    model = NewsOgTag


class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsOgTagInline, ]
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }


class ExtraMetaTagInline(admin.StackedInline):
    model = ExtraMetaTag


class OgTagAdmin(admin.ModelAdmin):
    inlines = [ExtraMetaTagInline, ]

admin.site.register(News, NewsAdmin)
admin.site.register(Tags)
admin.site.register(HashtagImg)
admin.site.register(OgTag, OgTagAdmin)
