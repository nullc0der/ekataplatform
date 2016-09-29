from django.conf.urls import url
from messagingsystem import views


urlpatterns = [
    url(r'^$', views.messaging_index, name='index'),
    url(r'^chat/(?P<chat_id>\d+)/$', views.get_chat, name='getchat'),
    url(r'^sendmessage/(?P<chat_id>\d+)/$', views.send_message, name='send'),
    url(r'^initmessage/(?P<to_user>\d+)/$', views.create_chat, name='create'),
    url(r'^setmessagestatus', views.set_message_status, name='setstatus'),
]
