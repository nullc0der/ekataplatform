from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^$', views.dashboard_page, name='index'),
    url(r'^skip/$', views.skipped_tasks, name='skip'),
    url(r'^download_member_stats/$', views.download_member_stats, name='download_member_stats')
]
