from django.conf.urls import url
from useraccount import views


urlpatterns = [
    url(r'^$', views.account_page, name='index'),
    url(r'^transfer/$', views.transfer_page, name='transfer'),
    url(r'^transferunit/(?P<id>\d+)/$', views.transferunit, name='transferunit'),
    url(r'^requestunit/(?P<id>\d+)/$', views.requestunit, name='requestunit')
]
