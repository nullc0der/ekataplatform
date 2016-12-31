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
    url(r'^emailtemplates/$', views.emailtemplates_page, name='emailtemplates'),
    url(r'^add_emailtemplate/$', views.add_emailtemplate, name='add_emailtemplate'),
    url(r'^delete_emailtemplate/$', views.delete_emailtemplate, name='delete_emailtemplate'),
    url(r'^edit_emailtemplate/(?P<id>\d+)/$', views.edit_emailtemplate, name='edit_emailtemplate'),
    url(r'^preview_emailtemplate/(?P<id>\d+)/$', views.preview_emailtemplate, name='preview_emailtemplate'),
]
