# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-18 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usertimeline', '0011_auto_20161018_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertimeline',
            name='sysupdate_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
