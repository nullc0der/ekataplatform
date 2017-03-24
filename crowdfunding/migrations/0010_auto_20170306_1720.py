# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-06 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0009_crowdfund_thankyou_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='crowdfund',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crowdfund',
            name='introduction',
            field=models.TextField(blank=True, default='', help_text='Write a introduction'),
        ),
    ]
