from django.conf.urls import url
from django.views.generic import TemplateView
from autosignup import views

thankyou = TemplateView.as_view(template_name='autosignup/thankyou.html')

urlpatterns = [
    url(r'^$', views.index_page, name='index'),
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
        r'thankyou/$',
        thankyou,
        name='thankyou'
    )
]
