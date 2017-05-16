from django.conf.urls import url
from backupsystem import views

urlpatterns = [
    url(r'^$', views.index_page, name='index'),
    # url(r'^download/$', views.download_file, name='download'),
    url(r'^mbackup/$', views.manual_backup, name='mbackup'),
]
