# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-06 05:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profilesystem', '0014_auto_20160801_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserUIState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='uistate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
