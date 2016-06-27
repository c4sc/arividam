# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 21:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0014_auto_20160404_1908'),
        ('sites', '0003_auto_20160515_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCalendar',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('calendar_id', models.CharField(max_length=128)),
                ('colour', models.CharField(blank=True, max_length=6)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='googlecalendars', to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]