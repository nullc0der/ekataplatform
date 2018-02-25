from django.conf.urls import url
from notification.api_views import NotificationView, NotificationDetailView


urlpatterns = [
    url(r'^$', NotificationView.as_view()),
    url(r'^setread/$', NotificationDetailView.as_view())
]
