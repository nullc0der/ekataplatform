from django.conf.urls import url
from useraccount import views


urlpatterns = [
    url(r'^$', views.account_page, name='index'),
    url(r'^transfer/$', views.transfer_page, name='transfer'),
    url(r'^transferunit/(?P<id>\d+)/$', views.transferunit, name='transferunit'),
    url(r'^requestunit/(?P<id>\d+)/$', views.requestunit, name='requestunit'),
    url(r'^subscribe_ekata_units/$', views.subscribe_ekata_units, name='subscribe_ekata_units'),
    url(r'^ekata_units_info/$', views.ekata_units_info, name='ekata_units_info'),
    url(r'^get_new_address/$',
        views.get_account_new_address, name='get_new_address'),
    url(r'^ekata_units_admin/$', views.ekata_units_admin, name='ekata_units_admin'),
    url(r'^distribute_ekata_units/$', views.distribute_ekata_units, name='distribute_ekata_units'),
    url(r'^verify_dist_code/$', views.verify_dist_code, name='verify_dist_code'),
    url(r'^add_next_release/$', views.add_next_release, name='add_next_release'),
    url(r'^get_ekata_units_users/$', views.get_ekata_units_users, name='get_ekata_units_users'),
    url(r'^transfer_ekata_units/$', views.transfer_ekata_units, name='transfer_ekata_units')
]
