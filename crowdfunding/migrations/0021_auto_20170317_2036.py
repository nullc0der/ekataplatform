# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-17 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0020_auto_20170317_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crowdfund',
            name='default_note',
            field=models.CharField(blank=True, default='', help_text='Set a default note for the payment form', max_length=200, verbose_name='Default Note'),
        ),
        migrations.AlterField(
            model_name='crowdfund',
            name='introduction',
            field=models.TextField(blank=True, default='', help_text='Write a crowdfund introduction'),
        ),
        migrations.AlterField(
            model_name='crowdfund',
            name='thankyou_message',
            field=models.TextField(blank=True, default='Thank You', help_text='Customize the payment form thank you message', verbose_name='Thank You Message'),
        ),
    ]