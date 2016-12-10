# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autosignup', '0031_auto_20161208_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprovider',
            name='invite_code',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='accountprovider',
            name='invite_code_is_open',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
