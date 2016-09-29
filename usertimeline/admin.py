from django.contrib import admin
from usertimeline.models import UserTimeline, TimelineSetting

# Register your models here.
admin.site.register(UserTimeline)
admin.site.register(TimelineSetting)
