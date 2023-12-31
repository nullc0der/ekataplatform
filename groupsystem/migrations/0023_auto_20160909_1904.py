# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-09 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsystem', '0022_auto_20160909_0724'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basicgroup',
            options={'permissions': (('can_access_admin', 'Can access admin'), ('can_read_news', 'Can read news'), ('can_create_news', 'Can create news'), ('can_update_news', 'Can update news'), ('can_delete_news', 'Can delete news'), ('can_read_post', 'Can read post'), ('can_create_post', 'Can create post'), ('can_update_post', 'Can update post'), ('can_approve_post', 'Can approve post'), ('can_delete_post', 'Can delete post'), ('can_read_comment', 'Can read comment'), ('can_create_comment', 'Can create comment'), ('can_update_comment', 'Can update comment'), ('can_approve_comment', 'Can approve comment'), ('can_delete_comment', 'Can delete comment'), ('can_like_post', 'Can like post'), ('can_create_notification', 'Can create notification'), ('can_create_invite', 'Can create invite'), ('can_add_member', 'Can add member'), ('can_remove_member', 'Can remove member'), ('can_ban_member', 'Can ban member'), ('can_lift_member_ban', 'Can lift member ban'), ('can_change_member_role', 'Can change member role'), ('can_edit_member_permission', 'Can edit member permission'), ('can_read_events', 'Can read events'), ('can_create_events', 'Can create events'), ('can_update_events', 'Can update events'), ('can_delete_events', 'Can delete events'), ('can_read_joinrequest', 'Can read join requests'), ('can_approve_joinrequest', 'Can approve join requests'), ('can_deny_joinrequest', 'Can deny joinrequest'), ('can_edit_group_profile', 'Can edit group profile'), ('can_read_role', 'Can read role'), ('can_read_custom_role', 'Can read custom role'), ('can_update_custom_role', 'Can update custom role'), ('can_create_custom_role', 'Can create custom role'))},
        ),
        migrations.AddField(
            model_name='customrole',
            name='can_change_member_role',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customrole',
            name='can_edit_member_permission',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupmemberextraperm',
            name='can_change_member_role',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupmemberextraperm',
            name='can_edit_member_permission',
            field=models.BooleanField(default=False),
        ),
    ]
