# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-28 19:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eblast', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailgroup',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='emailgroups', to=settings.AUTH_USER_MODEL, verbose_name='Site user'),
        ),
    ]
