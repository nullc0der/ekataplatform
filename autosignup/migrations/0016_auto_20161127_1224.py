# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-27 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autosignup', '0015_historicalcommunitysignup'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitysignup',
            name='approval_mail_sent',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='historicalcommunitysignup',
            name='approval_mail_sent',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]