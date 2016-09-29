# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-03 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usertimeline', '0008_auto_20160805_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertimeline',
            name='group_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='usertimeline',
            name='group_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='usertimeline',
            name='timeline_type',
            field=models.IntegerField(choices=[(1, 'transfer'), (2, 'request'), (3, 'release'), (4, 'verified'), (5, 'unverified'), (6, 'connection'), (7, 'groupinvites')]),
        ),
    ]
