# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-30 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysadmin', '0027_auto_20161030_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailid',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='emailid',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]