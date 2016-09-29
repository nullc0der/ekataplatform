# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 08:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groupsystem', '0009_joinrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicgroup',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribed_group', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='basicgroup',
            name='members',
            field=models.ManyToManyField(related_name='joined_group', to=settings.AUTH_USER_MODEL),
        ),
    ]
