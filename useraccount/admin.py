from django.contrib import admin
from useraccount.models import UserAccount, IncomeRelease, RequestUnits
# Register your models here.


admin.site.register(UserAccount)
admin.site.register(IncomeRelease)
admin.site.register(RequestUnits)
