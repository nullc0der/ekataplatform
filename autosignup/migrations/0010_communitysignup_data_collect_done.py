# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-19 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autosignup', '0009_auto_20161119_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitysignup',
            name='data_collect_done',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]