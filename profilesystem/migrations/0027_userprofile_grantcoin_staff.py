# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-18 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilesystem', '0026_remove_userprofile_grantcoin_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='grantcoin_staff',
            field=models.BooleanField(default=False),
        ),
    ]
