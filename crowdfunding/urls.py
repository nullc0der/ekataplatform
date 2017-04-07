from django.conf.urls import url
from crowdfunding import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accept_payment/$', views.accept_payment, name='accept_payment'),
    url(r'^admin/$', views.crowdfund_admin, name='crowdfund_admin'),
    url(r'^admin/start_crowdfund/$', views.start_crowdfund, name='start_crowdfund'),
    url(r'^admin/update_crowdfund/$', views.update_crowdfund, name='update_crowdfund'),
    url(r'^admin/payment_details/$', views.payment_details, name='payment_details'),
    url(r'^admin/add_predefined_amount/$', views.add_predefined_amount, name='add_predefined_amount'),
    url(r'^admin/add_product_feature/$', views.add_product_feature, name='add_product_feature'),
    url(r'^admin/delete_product_feature/$', views.delete_product_feature, name='delete_product_feature'),
    url(r'^admin/upload_video/$', views.upload_video, name='upload_video'),
    url(r'^admin/upload_image/$', views.upload_image, name='upload_image'),
    url(r'^admin/update_cards_html/$', views.update_cards_html, name='update_cards_html'),
    url(r'^admin/add_meta_tags/$', views.add_meta_tags, name='add_meta_tags')
]
