# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 20:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTimeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeline_type', models.IntegerField(choices=[(1, 'transfer'), (2, 'request'), (3, 'release'), (4, 'verified'), (5, 'unverified')])),
                ('sender', models.CharField(default='', max_length=200)),
                ('sender_id', models.CharField(default='', max_length=200)),
                ('receiver', models.CharField(default='', max_length=200)),
                ('receiver_id', models.CharField(default='', max_length=200)),
                ('amount', models.IntegerField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timelines', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
