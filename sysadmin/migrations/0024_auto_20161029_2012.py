# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-29 20:12
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('sysadmin', '0023_auto_20161028_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailupdate',
            name='message',
            field=tinymce.models.HTMLField(),
        ),
    ]
