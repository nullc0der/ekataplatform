# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-13 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0014_auto_20170313_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ogtaglink',
            name='page',
            field=models.CharField(choices=[('index', 'index'), ('hashtag', 'hashtag'), ('news', 'news'), ('crowdfunding', 'crowdfunding')], max_length=40),
        ),
    ]
