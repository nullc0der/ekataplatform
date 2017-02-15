# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-15 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crowdfund',
            options={'get_latest_by': 'id'},
        ),
        migrations.AlterField(
            model_name='crowdfund',
            name='goal',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
    ]
