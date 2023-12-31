import os
import glob
from datetime import timedelta

from django.conf import settings
from django.core import management
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from backupsystem.models import Backup, NextBackup


def create_backup(manual=False):
    location = settings.DBBACKUP_STORAGE_OPTIONS['location']
    db_name = 'db-' + now().strftime("%Y-%m-%d-%H:%I")
    db_path = location + '/' + db_name + '.dump.gz'
    media_name = 'media-' + now().strftime("%Y-%m-%d-%H:%I")
    media_path = location + '/' + media_name + '.tar'
    management.call_command(
        'dbbackup',
        compress=True,
        output_path=db_path,
        interactive=False
    )
    d_backup = Backup(
        name=db_name,
        b_type='db',
        path=db_path
    )
    d_backup.save()
    management.call_command(
        'mediabackup',
        output_path=media_path,
        interactive=False
    )
    mediabackup = Backup(
        name=media_name,
        b_type='media',
        path=media_path
    )
    mediabackup.save()
    if not manual:
        backups = glob.glob(location + '/*.*')
        backups.remove(db_path)
        backups.remove(media_path)
        for backup in backups:
            os.remove(backup)
        next_on = now() + timedelta(days=1)
        try:
            nextbackup = NextBackup.objects.latest()
            nextbackup.next_on = next_on
            nextbackup.save()
        except ObjectDoesNotExist:
            nextbackup = NextBackup(next_on=next_on)
            nextbackup.save()
    return
