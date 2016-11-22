from django.conf.urls import url
from landing import views


urlpatterns = [
    url(r'^$', views.index_page, name='index'),
    url(r'^hashtag/$', views.hashtag_page, name='hashtag'),
    url(r'^news/$', views.news_page, name='newses'),
    url(r'^news/(?P<id>\d+)/$', views.news_detail_page, name='news_detail'),
    url(r'^getimage/$', views.getimage, name='getimage'),
    url(
        r'^author/(?P<username>\w+)/$',
        views.author_detail_page,
        name='authordetail'
    ),
    url(
        r'^contact/$',
        views.send_contact_request,
        name='sendcontactrequest'
    ),
    url(
        r'^getinvite/$',
        views.get_invitation_key,
        name='getinvite'
    ),
    url(
        r'getinviteapi/$',
        views.get_invitation_key_from_production
    ),
    url(
        r'^newsletter_signup/$',
        views.newsletter_signup,
        name='newsletter_signup'
    )
]
