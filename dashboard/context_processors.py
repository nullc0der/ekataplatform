from dashboard.models import VersionInfo
from django.core.exceptions import ObjectDoesNotExist


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
