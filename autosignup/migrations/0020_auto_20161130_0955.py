# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-30 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autosignup', '0019_approvedmailtemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountaddcontact',
            name='emailaddress',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email Address'),
        ),
    ]
