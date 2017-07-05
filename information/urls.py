from django.views.generic import TemplateView
from django.conf.urls import url
from django.conf import settings

from information.views import contact_page


information_page = TemplateView.as_view(template_name='information/index.html')

urlpatterns = [
    url(r'^contact/$', contact_page, name='contact'),
]

if settings.EKATA_SITE_TYPE == 'beta':
    urlpatterns += [
        url(r'^$', information_page, name='index'),
    ]
