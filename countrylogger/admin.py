from django.contrib import admin
from django_object_actions import DjangoObjectActions,\
 takes_instance_or_queryset
from countrylogger.models import UserCountry

# Register your models here.


class UserCountryAdmin(DjangoObjectActions, admin.ModelAdmin):
    actions = ['show_total_users']
    change_actions = ['show_total_users']

    @takes_instance_or_queryset
    def show_total_users(self, request, queryset):
        for country in queryset:
            total = country.users.all().count()
            self.message_user(
                request, '{} has {} user'.format(country.name, total))
    show_total_users.short_description = 'Show total users'
    show_total_users.label = 'Total Users'


admin.site.register(UserCountry, UserCountryAdmin)
