from django.contrib import admin
from .models import UserProfile, UserCompletionRing, UserUIState, UserOneSignal

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(UserCompletionRing)
admin.site.register(UserUIState)
admin.site.register(UserOneSignal)
