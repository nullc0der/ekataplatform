# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-23 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0021_auto_20170421_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomerelease',
            name='user',
        ),
        migrations.RemoveField(
            model_name='requestunits',
            name='reciever',
        ),
        migrations.RemoveField(
            model_name='requestunits',
            name='sender',
        ),
        migrations.DeleteModel(
            name='IncomeRelease',
        ),
        migrations.DeleteModel(
            name='RequestUnits',
        ),
    ]
