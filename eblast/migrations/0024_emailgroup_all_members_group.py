# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-07 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eblast', '0023_auto_20170106_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailgroup',
            name='all_members_group',
            field=models.BooleanField(default=False),
        ),
    ]
