# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-09 17:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupsystem', '0031_auto_20180209_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basicgroup',
            old_name='staff',
            new_name='staffs',
        ),
    ]
