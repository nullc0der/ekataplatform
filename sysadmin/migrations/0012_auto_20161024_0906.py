# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-24 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysadmin', '0011_auto_20161024_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailupdate',
            name='from_email',
            field=models.EmailField(choices=[('support@ekata.social', 'support@ekata.social'), ('news@ekata.social', 'news@ekata.social'), ('newsletter@ekata.social', 'newsletter@ekata.social')], max_length=254),
        ),
    ]
