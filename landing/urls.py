from django.conf.urls import url
from landing import views


urlpatterns = [
    url(r'^$', views.index_page, name='index'),
    url(r'^hashtag/$', views.hashtag_page, name='hashtag'),
    url(r'^news/$', views.news_page, name='newses'),
    url(r'^news/(?P<id>\d+)/$', views.news_detail_page, name='news_detail'),
    url(r'^getimage/$', views.getimage, name='getimage'),
]
