# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-12-23 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagingsystem', '0003_chatroom_unsubscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]