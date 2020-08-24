from django.conf.urls import url, include
from messagingsystem import api_views, views


urlpatterns = [
    url(r'^chatrooms/$', api_views.ChatRoomsView.as_view()),
    url(r'^chat/(?P<chat_id>\d+)/$', api_views.ChatRoomDetailsView.as_view()),
    url(r'^deletemessages/$', views.delete_messages),
    url(r'^settyping/$', views.set_typing_status)
]
