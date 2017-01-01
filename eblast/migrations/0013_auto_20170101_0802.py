# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-01 08:02
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eblast', '0012_auto_20170101_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcampaign',
            name='message',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='template',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
