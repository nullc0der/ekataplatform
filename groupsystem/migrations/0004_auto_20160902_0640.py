# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-02 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsystem', '0003_auto_20160901_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicgroup',
            name='group_type_other',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='basicgroup',
            name='group_type',
            field=models.CharField(choices=[('1', 'Art'), ('2', 'Activist'), ('3', 'Political'), ('4', 'News'), ('5', 'Business'), ('6', 'Government'), ('7', 'Other')], max_length=30),
        ),
    ]
