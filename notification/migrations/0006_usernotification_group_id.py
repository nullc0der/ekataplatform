# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-08 22:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_usernotification_timeline_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='group_id',
            field=models.CharField(default='', max_length=200),
        ),
    ]
