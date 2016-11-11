from django.contrib import admin
from emailtosms.models import CarrierCSV, Carrier, Verifier

# Register your models here.


class CarrierAdmin(admin.ModelAdmin):
    readonly_fields = ['verified', 'verified_times']
    ordering = ['-verified_times']
    list_filter = ['verified']
    search_fields = ['name', 'country']

admin.site.register(CarrierCSV)
admin.site.register(Carrier, CarrierAdmin)
