# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-17 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsystem', '0034_groupnotification_is_important'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicgroup',
            name='join_status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('request', 'Request'), ('invite', 'Invite')], default='open', max_length=30),
        ),
    ]
