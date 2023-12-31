# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-28 21:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysadmin', '0020_auto_20161028_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailgroup',
            name='to_users',
            field=models.ManyToManyField(help_text="Site user's email id will be extracted by system automatically", to=settings.AUTH_USER_MODEL, verbose_name='Site user'),
        ),
    ]
