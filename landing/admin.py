from django.contrib import admin

from landing.models import\
    News, Tags, HashtagImg, GlobalOgTag, ExtraMetaTag, OgTagLink


# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on')
    search_fields = ('title',)
    ordering = ('-created_on',)
    list_filter = ('tags', )

    def get_queryset(self, request):
        qs = super(NewsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class ExtraMetaTagInline(admin.StackedInline):
    model = ExtraMetaTag


class GlobalOgTagAdmin(admin.ModelAdmin):
    inlines = [ExtraMetaTagInline, ]

admin.site.register(News, NewsAdmin)
admin.site.register(HashtagImg)
admin.site.register(GlobalOgTag, GlobalOgTagAdmin)
admin.site.register(OgTagLink)
