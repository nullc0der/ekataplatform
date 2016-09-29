from django.conf.urls import url
from invitationsystem.views import index_page

urlpatterns = [
    url(r'^$', index_page, name='index'),
]
