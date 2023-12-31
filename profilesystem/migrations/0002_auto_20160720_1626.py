# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 16:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profilesystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_office', models.CharField(blank=True, default='', max_length=20)),
                ('phone_home', models.CharField(blank=True, default='', max_length=20)),
                ('phone_mobile', models.CharField(blank=True, default='', max_length=20)),
                ('phone_emergency', models.CharField(blank=True, default='', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='phone', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_emergency',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_home',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_mobile',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_office',
        ),
    ]
