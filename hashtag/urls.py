from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from hashtag import views

hashtag_page = login_required(
    TemplateView.as_view(
        template_name='hashtag/index.html'
    )
)

urlpatterns = [
    url(r'^create/$', hashtag_page, name='index'),
    url(r'^getfacebook/$', views.get_facebook_account, name='getfacebook'),
    url(r'^gettwitter/$', views.get_twitter_account, name='gettwitter'),
    url(r'^uploadtwitter/$', views.upload_to_twitter, name='uploadtwitter'),
    url(r'^getimages/$', views.get_images, name='getimages'),
    url(r'^savehashtag/$', views.save_hashtag, name='savehashtag')
]
