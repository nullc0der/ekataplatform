# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-20 22:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autosignup', '0014_auto_20161120_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCommunitySignup',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('community', models.CharField(choices=[('grantcoin', 'grantcoin')], editable=False, max_length=100)),
                ('useraddress_in_db', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('useremail', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('userphone', models.CharField(blank=True, default='', max_length=20, verbose_name='Phone')),
                ('useraddress_from_twilio', models.TextField(blank=True, null=True)),
                ('useraddress_from_geoip', models.TextField(blank=True, null=True)),
                ('userimage', models.TextField(blank=True, max_length=100, null=True)),
                ('step_1_done', models.BooleanField(default=False, editable=False)),
                ('step_2_done', models.BooleanField(default=False, editable=False)),
                ('step_3_done', models.BooleanField(default=False, editable=False)),
                ('additional_step_done', models.BooleanField(default=False, editable=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending', max_length=100)),
                ('failed_auto_signup', models.BooleanField(default=False, editable=False)),
                ('sent_to_community_staff', models.BooleanField(default=False, editable=False)),
                ('auto_signup_fail_reason', models.CharField(default='', editable=False, max_length=200)),
                ('email_in_globaldb', models.BooleanField(default=False, editable=False)),
                ('phone_in_globaldb', models.BooleanField(default=False, editable=False)),
                ('data_collect_done', models.BooleanField(default=False, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical community signup',
            },
        ),
    ]
