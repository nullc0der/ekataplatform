# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0010_auto_20160716_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='next_release',
            field=models.DateField(),
        ),
    ]
