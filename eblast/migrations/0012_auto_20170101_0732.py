# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-01 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eblast', '0011_emailtemplate_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcampaign',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='template',
            field=models.TextField(blank=True, null=True),
        ),
    ]