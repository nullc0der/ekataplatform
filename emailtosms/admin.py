from django.contrib import admin
from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from emailtosms.models import CarrierCSV, Carrier, Verifier, UserCarrier

# Register your models here.


class CarrierAdmin(admin.ModelAdmin):
    readonly_fields = ['verified', 'verified_times']
    ordering = ['-verified_times']
    list_filter = ['verified']
    search_fields = ['name', 'country']


class UserCarrierAdmin(DjangoObjectActions, admin.ModelAdmin):
    actions = ['add_to_carrier']
    change_actions = ['add_to_carrier']
    readonly_fields = ['added_to_carrier']

    @takes_instance_or_queryset
    def add_to_carrier(self, request, queryset):
        count = 0
        for usercarrier in queryset:
            carrier, created = Carrier.objects.get_or_create(
                name=usercarrier.name,
                country=usercarrier.country,
                emailaddress=usercarrier.emailaddress
            )
            carrier.save()
            usercarrier.added_to_carrier = True
            usercarrier.save()
            count += 1
        self.message_user(request, '%s user requested carrier added to carrier list' % count)
    add_to_carrier.short_description = 'Add to carrier list'
    add_to_carrier.label = 'Add to carrier list'


class VerifierAdmin(admin.ModelAdmin):
    list_filter = ['failed']
    search_fields = ['user']
    readonly_fields = ['failed']

admin.site.register(CarrierCSV)
admin.site.register(Carrier, CarrierAdmin)
admin.site.register(UserCarrier, UserCarrierAdmin)
admin.site.register(Verifier, VerifierAdmin)
