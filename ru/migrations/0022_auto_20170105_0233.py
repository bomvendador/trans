# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-04 23:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0021_auto_20170105_0230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderstatus',
            old_name='position',
            new_name='position_n',
        ),
    ]
