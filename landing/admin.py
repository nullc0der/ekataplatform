from django.contrib import admin

from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from landing.models import\
    News, Tags, HashtagImg, GlobalOgTag, ExtraMetaTag, OgTagLink


# Register your models here.
class NewsAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('title', 'created_on')
    search_fields = ('title',)
    ordering = ('-created_on',)
    list_filter = ('tags', )
    readonly_fields = ('draft', )
    change_actions = ['publish', 'unpublish']
    actions = ['publish', 'unpublish']

    @takes_instance_or_queryset
    def publish(self, request, queryset):
        count = 0
        for news in queryset:
            news.draft = False
            news.save()
            count += 1
        self.message_user(
            request,
            '%s news published' % count
        )
    publish.short_description = 'Publish'
    publish.label = 'Publish'

    @takes_instance_or_queryset
    def unpublish(self, request, queryset):
        count = 0
        for news in queryset:
            news.draft = True
            news.save()
            count += 1
        self.message_user(
            request,
            '%s news unpublished' % count
        )
    unpublish.short_description = 'Unpublish'
    unpublish.label = 'Unpublish'

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
