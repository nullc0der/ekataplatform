# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-28 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autosignup', '0017_auto_20161128_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitysignup',
            name='distance_db_vs_geoip',
            field=models.CharField(default='', editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='communitysignup',
            name='distance_db_vs_twilio',
            field=models.CharField(default='', editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='historicalcommunitysignup',
            name='distance_db_vs_geoip',
            field=models.CharField(default='', editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='historicalcommunitysignup',
            name='distance_db_vs_twilio',
            field=models.CharField(default='', editable=False, max_length=100),
        ),
    ]