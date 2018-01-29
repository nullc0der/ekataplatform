from django.conf.urls import url

from groupsystem import api_views

urlpatterns = [
    url(r'^$', api_views.GroupsView.as_view())
]
