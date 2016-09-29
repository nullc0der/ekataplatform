from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from profilesystem import views


urlpatterns = [
    url(r'^$', views.index_page, name='index'),
    url(
        r'^personalinfo/$',
        login_required(TemplateView.as_view(template_name='profilesystem/pinfo.html')),
        name='personalinfo'
    ),
    url(r'^personalinfoedit/$', views.pinfo_edit_page, name='pedit'),
    url(
        r'^contact/$',
        login_required(TemplateView.as_view(template_name='profilesystem/contact.html')),
        name='contact'
    ),
    url(r'^contactedit/$', views.phone_edit_page, name='cedit'),
    url(
        r'^address/$',
        login_required(TemplateView.as_view(template_name='profilesystem/address.html')),
        name='address'
    ),
    url(r'^documents/$', views.document_page, name='documents'),
    url(r'^linkedaccount/$', views.social_account_page, name='linkedaccount'),
    url(r'^addressedit/$', views.address_edit_page, name='aedit'),
    url(
        r'^references/$',
        login_required(TemplateView.as_view(template_name='profilesystem/reference.html')),
        name='references'
    ),
    url(
        r'^useremailaddress/$',
        login_required(TemplateView.as_view(template_name='profilesystem/emailaddress.html')),
        name='emailaddress'
    ),
    url(r'^uploadavatar/$', views.upload_avatar, name='uploadavatar'),
    url(r'^setting/$', views.settings, name='setting'),
    url(r'^uploadfile/$', views.upload_file, name='uploadfile'),
    url(r'^queryavatar/$', views.query_avatar, name='queryavatar'),
    url(r'^setui/$', views.setuistate, name='setui'),
    url(r'^getui/$', views.getuistate, name='getui'),
    url(r'^setonline/$', views.set_onlinestate, name='setonline'),
    url(r'^saveonesignal/$', views.saveonesignal_id, name='onesignal')
]
