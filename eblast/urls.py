from django.conf.urls import url
from eblast import views


urlpatterns = [
    url(r'^emailgroups/$', views.emailgroups_page, name='emailgroups'),
    url(r'^create_emailgroup/$', views.create_emailgroup, name='create_emailgroup'),
    url(r'^delete_emailgroup/$', views.delete_emailgroup, name='delete_emailgroup'),
    url(r'^edit_emailgroup/(?P<id>\d+)/$', views.edit_emailgroup, name='edit_emailgroup'),
    url(r'^remove_emailid/$', views.remove_emailid, name='remove_emailid'),
    url(r'^unsubscribe_emailid/$', views.unsubscribe_emailid, name='unsubscribe_emailid'),
    url(r'^subscribe_emailid/$', views.subscribe_emailid, name='subscribe_emailid'),
]
