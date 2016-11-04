from django.conf.urls import url
from autosignup import views

urlpatterns = [
    url(r'^$', views.index_page, name='index')
]
