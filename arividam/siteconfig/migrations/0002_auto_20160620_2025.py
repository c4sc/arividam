# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteconfig', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='school_code',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='school_type',
            field=models.CharField(blank=True, choices=[('hs-govt', 'HS - Govt'), ('hs-aided', 'HS - Aided'), ('hs-unaided', 'HS - Unaided'), ('hss-govt', 'HSS - Govt'), ('hss-aided', ' HSS - Aided'), ('hss-unaided', 'HSS - Unaided')], max_length=20),
        ),
    ]