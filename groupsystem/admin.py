from django.contrib import admin
from groupsystem.models import BasicGroup, GroupNews, GroupNotification, GroupEvent, GroupPost, PostComment, JoinRequest, CustomRole, GroupMemberRole
# Register your models here.


admin.site.register(BasicGroup)
admin.site.register(GroupNews)
admin.site.register(GroupNotification)
admin.site.register(GroupEvent)
admin.site.register(GroupPost)
admin.site.register(PostComment)
admin.site.register(JoinRequest)
admin.site.register(CustomRole)
admin.site.register(GroupMemberRole)
