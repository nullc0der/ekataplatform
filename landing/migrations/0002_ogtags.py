# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OgTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('1', 'index'), ('2', 'hashtag'), ('3', 'news')], max_length=10)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=b'')),
            ],
        ),
    ]
