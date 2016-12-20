from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']


admin.site.register(UserProfile, UserProfileAdmin)
