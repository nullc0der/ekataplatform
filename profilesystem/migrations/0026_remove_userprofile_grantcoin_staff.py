# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-17 20:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profilesystem', '0025_userprofile_grantcoin_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='grantcoin_staff',
        ),
    ]