# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 22:02
from __future__ import unicode_literals

from django.db import migrations

def create_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_models("contenttypes", "ContentType")
    Page = ContentType.objects.get(app_label="cms", model="page")
    GlobalPagePermission = ContentType.objects.get(app_label="cms", model="globalpagepermission")

    editor,_ = Group.objects.get_or_create(name="Editor")
    editor.permissions.add(Permission.objects.filter(content_type=page, codename__in=['add_page','change_page','delete_page']))

def remove_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=['Editor','Writer']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160515_1433'),
    ]

    operations = [
        #migrations.RunPython(create_default_groups, remove_default_groups)
    ]