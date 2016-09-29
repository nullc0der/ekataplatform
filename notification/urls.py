from django.conf.urls import url
from notification import views


urlpatterns = [
    url(r'^$', views.notifications_view, name='index'),
]
