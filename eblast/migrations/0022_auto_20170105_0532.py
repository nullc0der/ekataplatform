# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-05 05:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eblast', '0021_auto_20170102_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailgroup',
            name='basic_group',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='groupsystem.BasicGroup', verbose_name='Link to Group'),
        ),
    ]