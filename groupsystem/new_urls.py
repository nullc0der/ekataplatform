from django.conf.urls import url
from groupsystem import new_views
from ekatadeveloper import views


urlpatterns = [
    url(r'^$', views.ReactIndexView.as_view()),
    url(r'^(?P<group_id>\d+)/posts/$',
        new_views.GroupMemberViews.as_view()),
    url(
        r'^(?P<group_id>\d+)/members/$',
        new_views.GroupMemberViews.as_view()),
    url(
        r'^(?P<group_id>\d+)/members/management/$',
        new_views.GroupAdminViews.as_view()),
    url(
        r'^(?P<group_id>\d+)/profile/$',
        new_views.GroupAdminViews.as_view())
]
