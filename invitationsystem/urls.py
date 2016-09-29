from django.conf.urls import url
from invitationsystem import views

urlpatterns = [
    url(r'^$', views.index_page, name='index'),
    url(r'^addinvitation/$', views.invitation_id_page, name='addinvitation')
]
