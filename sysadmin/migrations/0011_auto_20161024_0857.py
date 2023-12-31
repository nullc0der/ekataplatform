# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-24 08:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sysadmin', '0010_auto_20161023_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='emailupdate',
            name='to_users',
        ),
        migrations.AddField(
            model_name='emailupdate',
            name='to_groups',
            field=models.ManyToManyField(to='sysadmin.EmailGroup'),
        ),
    ]
