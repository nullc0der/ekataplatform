from sysadmin.models import SystemUpdate
from profilesystem.models import ReadSysUpdate


def get_sytemupdate(request):
    update = SystemUpdate.objects.filter(show=True).order_by('-timestamp')
    update_filtered = []
    if request.user.is_authenticated():
        readsysupadates = ReadSysUpdate.objects.filter(user=request.user)
        readsysupadates_ids = []
        for readsysupadate in readsysupadates:
            readsysupadates_ids.append(readsysupadate.sysupdate)
        if readsysupadates:
            for i in update:
                if i.id not in readsysupadates_ids:
                    update_filtered.append(i)
        else:
            update_filtered = update
    if update_filtered:
        updates = update_filtered[:3]
    else:
        updates = None
    return {
        'UPDATES': updates
    }
