# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-06 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitationsystem', '0004_auto_20161006_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='invitation_id',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='sent',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
