# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-31 17:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0011_auto_20161029_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL),
        ),
    ]
