from django.conf.urls import url
from taigaissuecreator import views


urlpatterns = [
    url(r'^$', views.post_issue, name='postissue')
]
