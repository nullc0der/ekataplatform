from django.conf.urls import url
from publicusers import views

urlpatterns = [
    url(r'^$', views.users_page, name='index'),
    url(r'^user/(?P<id>\d+)/$', views.user_details_page, name='user'),
    url(r'^sendsub/$', views.send_sub_connection, name='sendsub'),
    url(
        r'^requestconn/(?P<user>\d+)/$',
        views.request_connection,
        name='reqconn'
    ),
    url(
        r'^cancelreject/(?P<conn_id>\d+)/$',
        views.cancel_reject_connection,
        name='conncancelreject'
    ),
    url(
        r'^acceptconn/(?P<conn_id>\d+)/$',
        views.accept_connection,
        name='acceptconnection'
    ),
    url(
        r'connection/$',
        views.show_connection,
        name='showconn'
    ),
    url(
        r'getonlinestate/(?P<id>\d+)/$',
        views.get_onlinestate,
        name='getonline'
    ),
    url('getonlineusers', views.get_onlineusers, name='getonlineusers')
]
