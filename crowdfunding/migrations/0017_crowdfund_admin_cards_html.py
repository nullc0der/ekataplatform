# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-11 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0016_crowdfund_cards_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='crowdfund',
            name='admin_cards_html',
            field=models.TextField(blank=True, default=''),
        ),
    ]
