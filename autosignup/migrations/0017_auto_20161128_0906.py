# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-28 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupsystem', '0027_auto_20161016_1923'),
        ('autosignup', '0016_auto_20161127_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprovider',
            name='allowed_distance',
            field=models.IntegerField(blank=True, default=20),
        ),
        migrations.AddField(
            model_name='accountprovider',
            name='basicgroup',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='groupsystem.BasicGroup'),
        ),
    ]