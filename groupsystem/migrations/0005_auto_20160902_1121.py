# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-02 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsystem', '0004_auto_20160902_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicgroup',
            name='group_type_other',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Please Specify'),
        ),
    ]
