# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-07 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupsystem', '0018_groupmemberrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmemberrole',
            name='basic_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberrole', to='groupsystem.BasicGroup'),
        ),
    ]
