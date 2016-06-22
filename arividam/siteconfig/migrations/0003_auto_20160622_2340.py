# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 18:10
from __future__ import unicode_literals

import arividam.siteconfig.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteconfig', '0002_auto_20160620_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='banner_logo',
            field=models.ImageField(blank=True, upload_to=arividam.siteconfig.models.banner_path),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='school_type',
            field=models.CharField(blank=True, choices=[('hs-govt', 'HS - Govt'), ('hs-aided', 'HS - Aided'), ('hs-unaided', 'HS - Unaided'), ('hss-govt', 'HSS - Govt'), ('hss-aided', 'HSS - Aided'), ('hss-unaided', 'HSS - Unaided'), ('vhse-govt', 'VHSE - Govt'), ('vhse-aided', 'VHSE - Aided'), ('vhse-unaided', 'VHSE - Unaided')], max_length=20),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='site_css',
            field=models.FileField(blank=True, upload_to=arividam.siteconfig.models.site_css_path),
        ),
    ]
