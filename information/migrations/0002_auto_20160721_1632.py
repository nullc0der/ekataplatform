# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='contact',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='contact',
            name='telephone_no',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
