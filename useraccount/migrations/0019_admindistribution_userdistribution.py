# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-21 11:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('useraccount', '0018_distributeverification'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminDistribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField()),
                ('no_of_accout', models.PositiveIntegerField()),
                ('total_amount', models.FloatField()),
                ('amount_per_user', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserDistribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distribution', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
