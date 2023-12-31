# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 07:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profilesystem.models
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_number', models.CharField(blank=True, default='', max_length=10, verbose_name='House Number')),
                ('street', models.CharField(blank=True, default='', max_length=200, verbose_name='street')),
                ('zip_code', models.CharField(blank=True, default='', max_length=10, verbose_name='zip code')),
                ('city', models.CharField(blank=True, default='', max_length=100, verbose_name='city')),
                ('state', models.CharField(blank=True, default='', max_length=100, verbose_name='state')),
                ('country', models.CharField(blank=True, default='', max_length=100, verbose_name='country')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to=profilesystem.models.get_upload_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', versatileimagefield.fields.VersatileImageField(upload_to='avatar', verbose_name='user avatar')),
                ('title', models.CharField(default='user', max_length=100)),
                ('website', models.URLField(blank=True, default='')),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], default='', max_length=1)),
                ('account_type', models.CharField(blank=True, default='personal', max_length=100)),
                ('activation_key', models.CharField(blank=True, default='', max_length=40)),
                ('email_verified', models.BooleanField(default=False)),
                ('phone_office', models.CharField(blank=True, default='', max_length=20)),
                ('phone_home', models.CharField(blank=True, default='', max_length=20)),
                ('phone_mobile', models.CharField(blank=True, default='', max_length=20)),
                ('phone_emergency', models.CharField(blank=True, default='', max_length=20)),
                ('name_public', models.BooleanField(default=True)),
                ('website_public', models.BooleanField(default=True)),
                ('gender_public', models.BooleanField(default=True)),
                ('business_public', models.BooleanField(default=True)),
                ('location_public', models.BooleanField(default=True)),
                ('avatar_public', models.BooleanField(default=True)),
                ('phone_public', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profile',
            },
        ),
    ]
