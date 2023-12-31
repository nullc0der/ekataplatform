from django.conf.urls import url, include

from groupsystem import api_views

urlpatterns = [
    url(r'^$', api_views.GroupsView.as_view()),
    url(r'^(?P<group_id>\d+)/details/$', api_views.GroupDetailView.as_view()),
    url(
        r'^subscribe/(?P<group_id>\d+)/$',
        api_views.GroupSubscribeView.as_view()),
    url(r'create/$', api_views.CreateGroupView.as_view()),
    url(
        r'^join/(?P<group_id>\d+)/$',
        api_views.JoinGroupView.as_view()),
    url(r'^(?P<group_id>\d+)/members/$',
        api_views.GroupMembersView.as_view()),
    url(r'^(?P<group_id>\d+)/members/management/$',
        api_views.GroupMembersManagementView.as_view()),
    url(r'^(?P<group_id>\d+)/joinrequests/$',
        api_views.GroupJoinRequestView.as_view()),
    url(r'^(?P<group_id>\d+)/members/(?P<member_id>\d+)/changerole/$',
        api_views.GroupMemberChangeRoleView.as_view()),
    url(r'^(?P<group_id>\d+)/joinrequests/(?P<request_id>\d+)/$',
        api_views.GroupJoinRequestApproveView.as_view()),
    url(r'^(?P<group_id>\d+)/roles/$',
        api_views.GroupMemberPermission.as_view()),
    url(r'^(?P<group_id>\d+)/settings/$',
        api_views.GroupSettingsView.as_view()),
    url(r'^(?P<group_id>\d+)/notifications/$',
        api_views.GroupNotificationsView.as_view()),
    url(r'^(?P<group_id>\d+)/mynotifications/$',
        api_views.GroupMemberNotificationView.as_view()),
    url(r'^(?P<group_id>\d+)/invitemember/$',
        api_views.InviteMemberView.as_view()),
    url(r'^acceptinvite/$',
        api_views.InviteAction.as_view()),
    url(r'^(?P<group_id>\d+)/requestdelete/$',
        api_views.RequestDeleteGroup.as_view()),
    url(r'^posts/', include('grouppost.urls'))
]
