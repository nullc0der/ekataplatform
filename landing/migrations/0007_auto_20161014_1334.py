# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_auto_20161014_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ogtag',
            name='page',
            field=models.CharField(choices=[('index', 'index'), ('hashtag', 'hashtag'), ('news', 'news')], max_length=10),
        ),
    ]