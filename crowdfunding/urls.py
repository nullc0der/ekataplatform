from django.conf.urls import url
from crowdfunding import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accept_payment/$', views.accept_payment, name='accept_payment'),
    url(r'^admin/$', views.crowdfund_admin, name='crowdfund_admin'),
    url(r'^admin/start_crowdfund/$', views.start_crowdfund, name='start_crowdfund'),
    url(r'^admin/update_crowdfund/$', views.update_crowdfund, name='update_crowdfund'),
    url(r'^admin/payment_details/$', views.payment_details, name='payment_details')
]
