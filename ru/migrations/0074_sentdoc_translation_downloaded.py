# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-22 00:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0073_auto_20170119_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentdoc',
            name='translation_downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
