# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 13:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profilesystem', '0011_auto_20160729_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercompletionring',
            old_name='skipped_lists',
            new_name='skipped_list',
        ),
    ]
