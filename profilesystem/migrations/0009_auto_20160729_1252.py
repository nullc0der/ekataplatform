# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 12:52
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profilesystem', '0008_auto_20160729_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercompletionring',
            name='skipped_list',
            field=jsonfield.fields.JSONField(),
        ),
    ]
