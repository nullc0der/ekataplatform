# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitationsystem', '0007_auto_20161203_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='invitation_type',
            field=models.CharField(choices=[('default', 'default'), ('grantcoin', 'grantcoin')], default='default', editable=False, max_length=40),
        ),
    ]