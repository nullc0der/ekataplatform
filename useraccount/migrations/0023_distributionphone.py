# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-23 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0022_auto_20170423_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistributionPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(default='', help_text='please enter phone number with country code e.g +112345678', max_length=200)),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
    ]
