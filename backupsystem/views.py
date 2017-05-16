from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from backupsystem.models import Backup, NextBackup
from backupsystem.tasks import task_create_backup

# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def index_page(request):
    try:
        nextbackup = NextBackup.objects.latest()
    except ObjectDoesNotExist:
        nextbackup = None
    dbbackups = Backup.objects.filter(b_type='db').order_by('-id')
    mediabackups = Backup.objects.filter(b_type='media').order_by('-id')
    return render(
        request,
        'backupsystem/index.html',
        {
            'nextbackup': nextbackup,
            'dbbackups': dbbackups,
            'mediabackups': mediabackups
        }
    )


"""
@require_POST
@user_passes_test(lambda u: u.is_superuser)
def download_file(request):
    backup_id = request.POST.get('id')
    try:
        backup = Backup.objects.get(id=backup_id)
        response = HttpResponse(
            file(backup.path).read(), 'application/force-download')
        return response
    except ObjectDoesNotExist:
        return HttpResponse(status=500)
"""


@require_POST
@user_passes_test(lambda u: u.is_superuser)
def manual_backup(request):
    task_create_backup.delay(manual=True)
    return HttpResponse(status=200)
