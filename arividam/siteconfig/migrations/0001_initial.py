# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 13:55
from __future__ import unicode_literals

import arividam.siteconfig.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0003_auto_20160515_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_css', models.FileField(upload_to=arividam.siteconfig.models.site_css_path)),
                ('banner_logo', models.ImageField(upload_to=arividam.siteconfig.models.banner_path)),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='config', to='sites.Site')),
            ],
        ),
    ]