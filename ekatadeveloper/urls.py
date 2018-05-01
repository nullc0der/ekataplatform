"""ekatadeveloper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from allauth.socialaccount.views import ConnectionsView
from allauth.account.views import PasswordSetView, PasswordChangeView
from ekatadeveloper.views import send_menus

admin.site.site_title = 'Ekata administration'
admin.site.site_header = 'Ekata administration'
admin.site.index_title = 'Ekata administration'

disclaimer = TemplateView.as_view(template_name='account/disclaimer.html')
manifest = TemplateView.as_view(template_name='manifest.json')
updateworker = TemplateView.as_view(
    template_name='OneSignalSDKUpdaterWorker.js',
    content_type='application/javascript'
)
sdkworker = TemplateView.as_view(
    template_name='OneSignalSDKWorker.js',
    content_type='application/javascript'
)

urlpatterns = [
    url(r'manifest\.json', manifest),
    url(r'OneSignalSDKUpdaterWorker\.js', updateworker),
    url(r'OneSignalSDKWorker\.js', sdkworker),
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', logout, {'next_page': '/'}, name="logout"),
    url(r'^disconnect/$', ConnectionsView.as_view(success_url='/profile'), name='disconnect'),
    url(r'^setpassword/$', PasswordSetView.as_view(success_url='/profile'), name='setpassword'),
    url(r'^changepassword/$', PasswordChangeView.as_view(success_url='/profile'), name='changepassword'),
    url(r'^', include('landing.urls', namespace='landing')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^profile/', include('profilesystem.urls', namespace='profilesystem')),
    url(r'^members/', include('publicusers.urls', namespace='publicusers')),
    url(r'^information/', include('information.urls', namespace='information')),
    url(r'^disclaimer/', disclaimer, name='disclaimer'),
    url(r'^timeline/', include('usertimeline.urls', namespace='usertimeline')),
    url(r'^notification/', include('notification.urls', namespace='notification')),
    url(r'^messaging/', include('messagingsystem.urls', namespace='messaging')),
    url(r'^hashtag/', include('hashtag.urls', namespace='hashtag')),
    url(r'^type/', include('groupsystem.urls', namespace='g')),
    url(r'^emailtosms/', include('emailtosms.urls', namespace='emailtosms')),
    url(r'^eblast/', include('eblast.urls', namespace='eblast')),
    url(r'^getmenu/', send_menus, name='getmenu'),
    url(r'^crowdfunding/', include('crowdfunding.urls', namespace='crowdfunding')),
    url(r'^backups/', include('backupsystem.urls', namespace='backupsystem'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
