# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-20 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilesystem', '0022_auto_20161002_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio_public',
            field=models.BooleanField(default=True),
        ),
    ]
