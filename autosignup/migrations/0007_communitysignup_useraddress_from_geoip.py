# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-17 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autosignup', '0006_auto_20161114_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitysignup',
            name='useraddress_from_geoip',
            field=models.TextField(blank=True, null=True),
        ),
    ]
