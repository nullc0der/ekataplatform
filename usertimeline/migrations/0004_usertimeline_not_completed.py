# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usertimeline', '0003_usertimeline_instruction'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertimeline',
            name='not_completed',
            field=models.BooleanField(default=True),
        ),
    ]
