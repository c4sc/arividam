# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-10 14:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_googlecalendar', '0002_googlecalendar_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlecalendar',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_googlecalendar_googlecalendar', serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='googlecalendar',
            name='colour',
            field=models.CharField(blank=True, help_text='Colour in hex format: rrggbb', max_length=6),
        ),
    ]
