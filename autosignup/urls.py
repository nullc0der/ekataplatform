from django.conf.urls import url
from django.views.generic import TemplateView
from autosignup import views

thankyou = TemplateView.as_view(template_name='autosignup/thankyou.html')
signupclosed = TemplateView.as_view(template_name='autosignup/signupclosed.html')


urlpatterns = [
    # url(r'^$', views.index_page, name='index'),
    url(
        r'^getform/$',
        views.check_step,
        name='getform'
    ),
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
    url(
        r'^additional_step/(?P<id>\d+)/$',
        views.additional_step,
        name='additional_step'
    ),
    url(
        r'^thankyou/$',
        thankyou,
        name='thankyou'
    ),
    url(
        r'^signupclosed/$',
        signupclosed,
        name='signupclosed'
    ),
    url(
        r'^$',
        views.signups_page,
        name='signups'
    ),
    url(
        r'^delete_signup/$',
        views.delete_signup,
        name='delete_signup'
    ),
    url(
        r'^set_signup_status/$',
        views.set_signup_status,
        name='set_signup_status'
    ),
    url(
        r'^add_account/$',
        views.add_account,
        name='add_account'
    ),
    url(
        r'^edit_signup/(?P<id>\d+)/$',
        views.edit_signup,
        name='edit_signup'
    ),
    url(
        r'^filter_signup/$',
        views.filter_signup,
        name='filter_signup'
    ),
    url(
        r'^get_histories/(?P<id>\d+)/$',
        views.get_histories,
        name='get_histories'
    ),
    url(
        r'^get_history/(?P<id>\d+)/$',
        views.get_history,
        name='get_history'
    ),
    url(
        r'^revert_to_history/$',
        views.revert_to_history,
        name='revert_to_history'
    )
]