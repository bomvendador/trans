# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-13 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0064_auto_20170113_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentdoc',
            name='comments',
            field=models.BooleanField(default=False),
        ),
    ]
