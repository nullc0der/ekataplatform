# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-19 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profilesystem', '0030_userprofile_ekata_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='', max_length=2, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='state',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='street',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Street'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='zip_code',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='Zip Code'),
        ),
    ]
