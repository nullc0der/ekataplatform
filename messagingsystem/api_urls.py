from django.conf.urls import url, include
from messagingsystem import api_views


urlpatterns = [
    url(r'^chatrooms/$', api_views.ChatRoomsView.as_view()),
    url(r'^chat/(?P<chat_id>\d+)/$', api_views.ChatRoomDetailsView.as_view())
]
