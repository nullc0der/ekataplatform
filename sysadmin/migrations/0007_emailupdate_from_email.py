# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-12 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysadmin', '0006_auto_20161010_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailupdate',
            name='from_email',
            field=models.EmailField(default='support@ekata.social', max_length=254),
        ),
    ]
