from django.conf.urls import url

from groupsystem import api_views

urlpatterns = [
    url(r'^$', api_views.GroupsView.as_view()),
    url(
        r'^subscribe/(?P<group_id>\d+)/$',
        api_views.GroupSubscribeView.as_view()),
    url(r'create/$', api_views.CreateGroupView.as_view()),
    url(
        r'^join/(?P<group_id>\d+)/$',
        api_views.JoinGroupView.as_view()),
    url(r'^(?P<group_id>\d+)/members/$',
        api_views.GroupMembersView.as_view()),
    url(r'^(?P<group_id>\d+)/joinrequests/$',
        api_views.GroupJoinRequestView.as_view()),
    url(r'^(?P<group_id>\d+)/members/(?P<member_id>\d+)/changerole/$',
        api_views.GroupMemberChangeRoleView.as_view()),
    url(r'^(?P<group_id>\d+)/joinrequests/(?P<request_id>\d+)/$',
        api_views.GroupJoinRequestApproveView.as_view()),
    url(r'^(?P<group_id>\d+)/roles/$',
        api_views.GroupMemberPermission.as_view()),
]
