from django.conf.urls import url
from usertimeline import views


urlpatterns = [
    url(r'^$', views.timeline_page, name='index'),
    url(r'^setstate/$', views.set_timelinestate, name='state'),
    url(r'^search/$', views.search_timeline, name="search")
]
