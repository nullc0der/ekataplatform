from django.conf.urls import url
from notification import views


urlpatterns = [
    url(r'^$', views.notifications_view, name='index'),
    url(r'^setread/$', views.set_notificationread, name='setnotificationread'),
    url(r'^setallread/$', views.set_allnotificationsread, name='setallread')
]
