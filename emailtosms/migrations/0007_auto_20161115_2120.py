# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-15 21:20
from __future__ import unicode_literals

from django.db import migrations, models
import emailtosms.models


class Migration(migrations.Migration):

    dependencies = [
        ('emailtosms', '0006_auto_20161115_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifier',
            name='code',
            field=models.CharField(default=emailtosms.models.random_string, max_length=10),
        ),
    ]