# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-18 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0006_usernotification_group_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='sysupdate_message',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='sysupdate_timestamp',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='sysupdate_type',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='usernotification',
            name='notification_type',
            field=models.IntegerField(choices=[(1, 'transfer'), (2, 'request'), (3, 'release'), (4, 'verified'), (5, 'unverified'), (6, 'connectionreq'), (7, 'connectioncancel'), (8, 'connectionaccept'), (9, 'connectionreject'), (10, 'disconnect'), (11, 'groupinvite'), (12, 'groupjoinrequest'), (13, 'systemupdate')]),
        ),
    ]