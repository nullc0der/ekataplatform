# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 12:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_auto_20161014_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsOgTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=b'')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landing.News')),
            ],
        ),
    ]
