# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-21 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0020_nextrelease'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributeverification',
            name='code',
            field=models.CharField(max_length=8),
        ),
    ]