# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-09 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsystem', '0021_auto_20160909_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicgroup',
            name='group_type',
            field=models.CharField(choices=[('1', 'Art'), ('2', 'Activist'), ('3', 'Political'), ('4', 'News'), ('5', 'Business'), ('6', 'Government'), ('7', 'Blog'), ('8', 'Other')], max_length=30),
        ),
    ]
