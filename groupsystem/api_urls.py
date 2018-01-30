from django.conf.urls import url

from groupsystem import api_views

urlpatterns = [
    url(r'^$', api_views.GroupsView.as_view()),
    url(r'^subscribe/(?P<group_id>\d+)/$', api_views.GroupSubscribeView.as_view())
]
