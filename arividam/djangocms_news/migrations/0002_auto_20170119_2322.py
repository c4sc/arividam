# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-19 17:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotednews',
            name='page',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cms.Page'),
        ),
    ]
