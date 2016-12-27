from django.conf.urls import url
from eblast import views


urlpatterns = [
    url(r'^emailgroups/$', views.emailgroups_page, name='emailgroups')
]
