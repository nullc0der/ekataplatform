# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-09 17:54
from __future__ import unicode_literals

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('sysadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailupdate',
            name='message',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
