from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from landing.models import\
    News, Tags, HashtagImg, GlobalOgTag, ExtraMetaTag, OgTagLink


# Register your models here.
class ExtraMetaTagInline(admin.StackedInline):
    model = ExtraMetaTag


class GlobalOgTagAdmin(admin.ModelAdmin):
    inlines = [ExtraMetaTagInline, ]

admin.site.register(News, MarkdownxModelAdmin)
admin.site.register(HashtagImg)
admin.site.register(GlobalOgTag, GlobalOgTagAdmin)
admin.site.register(OgTagLink)
