# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-01 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autosignup', '0021_auto_20161201_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitysignup',
            name='not_verifiable_number',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='historicalcommunitysignup',
            name='not_verifiable_number',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
