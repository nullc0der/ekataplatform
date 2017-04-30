from django.conf.urls import url
from useraccount import views


urlpatterns = [
    url(r'^$', views.account_page, name='index'),
    url(r'^subscribe_ekata_units/$',
        views.subscribe_ekata_units, name='subscribe_ekata_units'),
    url(r'^ekata_units_info/$',
        views.ekata_units_info, name='ekata_units_info'),
    url(r'^get_new_address/$',
        views.get_account_new_address, name='get_new_address'),
    url(r'^grantcoin/distribution/$',
        views.ekata_units_admin, name='ekata_units_admin'),
    url(r'^distribute_ekata_units/$',
        views.distribute_ekata_units, name='distribute_ekata_units'),
    url(r'^verify_dist_code/$',
        views.verify_dist_code, name='verify_dist_code'),
    url(r'^add_next_release/$',
        views.add_next_release, name='add_next_release'),
    url(r'^get_ekata_units_users/$',
        views.get_ekata_units_users, name='get_ekata_units_users'),
    url(r'^transfer_ekata_units/$',
        views.transfer_ekata_units, name='transfer_ekata_units'),
    url(r'set_distribution_phone/$',
        views.set_distribution_phone, name='set_distribution_phone'),
    url(
        r'remove_codes/$',
        views.remove_codes, name='remove_codes'),
    url(
        r'single_dist/$',
        views.single_distribution, name='single_dist'),
    url(r'^verify_sdist_code/$',
        views.verify_sdist_code, name='verify_sdist_code'),
    url(r'^get_total_amount/$',
        views.get_total_amount, name='get_total_amount')
]
