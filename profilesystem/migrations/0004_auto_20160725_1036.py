# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilesystem', '0003_auto_20160725_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True),
        ),
    ]
