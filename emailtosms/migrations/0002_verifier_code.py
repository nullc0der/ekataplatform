# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-11 18:34
from __future__ import unicode_literals

from django.db import migrations, models
import invitationsystem.models


class Migration(migrations.Migration):

    dependencies = [
        ('emailtosms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifier',
            name='code',
            field=models.CharField(default=invitationsystem.models.random_string, max_length=10),
        ),
    ]
