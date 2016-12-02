# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-02 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invitationsystem', '0006_auto_20161006_2320'),
        ('autosignup', '0023_auto_20161202_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountprovidercsv',
            name='processed',
        ),
        migrations.AddField(
            model_name='accountprovidercsv',
            name='processed_to',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='accountprovidercsv',
            name='status',
            field=models.CharField(default='processing', max_length=100),
        ),
        migrations.AddField(
            model_name='communitysignup',
            name='invitation',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='invitationsystem.Invitation'),
        ),
        migrations.AddField(
            model_name='communitysignup',
            name='referred_by',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='historicalcommunitysignup',
            name='invitation',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='invitationsystem.Invitation'),
        ),
        migrations.AddField(
            model_name='historicalcommunitysignup',
            name='referred_by',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='accountprovidercsv',
            name='accountprovider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membercsvs', to='autosignup.AccountProvider'),
        ),
    ]