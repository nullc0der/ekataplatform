from django.conf.urls import url
from emailtosms import views


urlpatterns = [
    url(r'^$', views.emailtosms_page, name='index'),
    url(r'^add_verifier/$', views.add_verifier, name='add_verifier'),
    url(r'^verify_code/$', views.verify_code, name='verify_code'),
    url(r'^request_carrier/$', views.request_carrier, name='request_carrier')
]
