from django.conf.urls import url
from useraccount import views


urlpatterns = [
    url(r'^$', views.account_page, name='index'),
    url(r'^transfer/$', views.transfer_page, name='transfer'),
    url(r'^transferunit/(?P<id>\d+)/$', views.transferunit, name='transferunit'),
    url(r'^requestunit/(?P<id>\d+)/$', views.requestunit, name='requestunit'),
    url(r'^subscribe_ekata_units/$', views.subscribe_ekata_units, name='subscribe_ekata_units'),
    url(r'^ekata_units_info/$', views.ekata_units_info, name='ekata_units_info')
]
