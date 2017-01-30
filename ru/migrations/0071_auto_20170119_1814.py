# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-19 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0070_auto_20170119_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationtheme',
            name='short_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='translationtype',
            name='short_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='translationtype',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
