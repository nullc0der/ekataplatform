from dashboard.models import VersionInfo
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.urlresolvers import reverse


HOME = [
    reverse('dashboard:index')[3:],
    reverse('myaccount:index')[3:],
    reverse('profilesystem:index')[3:],
    reverse('usertimeline:index')[3:],
    reverse('messaging:index')[3:]
]

COMMUNITY = [
    reverse('publicusers:index')[3:],
    reverse('g:allgroups')[3:],
    reverse('g:joinedgroups')[3:],
    reverse('g:subscribedgroups')[3:],
    reverse('information:index')[3:],
    reverse('information:contact')[3:],
    reverse('crowdfunding:index')[3:],
    reverse('crowdfunding:crowdfund_admin')[3:],
    reverse('eblast:emailtemplates')[3:],
    reverse('eblast:emailgroups')[3:],
    reverse('eblast:emailcampaign_page')[3:],
    reverse('backupsystem:index')[3:],
]

APPS = [
    reverse('hashtag:index')[3:],
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
    if request.path[3:] in HOME:
        return {
            'ACTIVE_TAB': 'home',
            'TEMPLATE_NAME': 'sidebar_home.html'
        }
    if request.path[3:] in COMMUNITY:
        return {
            'ACTIVE_TAB': 'community',
            'TEMPLATE_NAME': 'sidebar_community.html'
        }
    if request.path[3:] in APPS:
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
