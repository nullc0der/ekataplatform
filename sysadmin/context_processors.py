from sysadmin.models import SystemUpdate


def get_sytemupdate(request):
    update = SystemUpdate.objects.filter(show=True).order_by('-timestamp')
    if update:
        updates = update[:3]
    else:
        updates = None
    return {
        'UPDATES': updates
    }
