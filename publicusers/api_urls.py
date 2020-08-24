from django.conf.urls import url, include
from publicusers import api_views


urlpatterns = [
    url(r'^$', api_views.UsersListView.as_view())
]
