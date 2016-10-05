# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-05 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0002_auto_20160721_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='VersionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(help_text='add bg-<coloname>', max_length=20)),
                ('version_number', models.CharField(max_length=20)),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
    ]
