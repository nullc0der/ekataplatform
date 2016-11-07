from django.conf.urls import url
from autosignup import views

urlpatterns = [
    url(r'^$', views.index_page, name='index'),
    url(
        r'^step_1_signup/(?P<id>\d+)/$',
        views.step_1_signup,
        name='step_1_signup'
    ),
    url(
        r'^step_2_signup/(?P<id>\d+)/$',
        views.step_2_signup,
        name='step_2_signup'
    ),
    url(
        r'^step_2_verification/(?P<id>\d+)/$',
        views.verify_email_code,
        name='step_2_verification'
    ),
    url(
        r'^step_3_signup/(?P<id>\d+)/$',
        views.step_3_signup,
        name='step_3_signup'
    ),
    url(
        r'^step_3_verification/(?P<id>\d+)/$',
        views.verify_phone_code,
        name='step_3_verification'
    ),
]
