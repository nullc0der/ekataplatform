from dashboard.models import VersionInfo
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.urlresolvers import reverse


HOME = [
    reverse('dashboard:index'),
    reverse('myaccount:index'),
    reverse('myaccount:transfer'),
    reverse('profilesystem:index'),
    reverse('usertimeline:index'),
    reverse('messaging:index')
]

COMMUNITY = [
    reverse('publicusers:index'),
    reverse('g:allgroups'),
    reverse('g:joinedgroups'),
    reverse('g:subscribedgroups'),
    reverse('information:index'),
    reverse('information:contact'),
    reverse('crowdfunding:index'),
    reverse('crowdfunding:crowdfund_admin'),
    reverse('eblast:emailtemplates'),
    reverse('eblast:emailgroups'),
    reverse('eblast:emailcampaign_page')
]

APPS = [
    reverse('hashtag:index'),
]


def version_info(request):
    try:
        version_info = VersionInfo.objects.latest()
        name = version_info.name
        color = version_info.color
        version_number = version_info.version_number
    except ObjectDoesNotExist:
        name = 'Experimental'
        color = 'bg-green'
        version_number = '1.2.4'
    return {
        'VERSION_NAME': name,
        'VERSION_COLOR': color,
        'VERSION_NUMBER': version_number
    }


def site_type(request):
    ekata_site_type = settings.EKATA_SITE_TYPE
    if ekata_site_type == 'beta':
        return {
            'SITE_TYPE': 'beta'
        }
    return {
        'SITE_TYPE': None
    }


def active_menu_tab(request):
    if request.path in HOME:
        return {
            'ACTIVE_TAB': 'home',
            'TEMPLATE_NAME': 'sidebar_home.html'
        }
    if request.path in COMMUNITY:
        return {
            'ACTIVE_TAB': 'community',
            'TEMPLATE_NAME': 'sidebar_community.html'
        }
    if request.path in APPS:
        return {
            'ACTIVE_TAB': 'apps',
            'TEMPLATE_NAME': 'sidebar_apps.html'
        }
    return {
        'ACTIVE_TAB': None,
        'TEMPLATE_NAME': None
    }


def last_accessed_group(request):
    if 'basicgroup' in request.session:
        return {
            'group': request.session['basicgroup']
        }
    return {
        'group': None
    }
