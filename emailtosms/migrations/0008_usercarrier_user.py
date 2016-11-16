# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-16 14:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emailtosms', '0007_auto_20161115_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercarrier',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_carrier', to=settings.AUTH_USER_MODEL),
        ),
    ]
