# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-13 12:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0058_auto_20170113_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager',
            old_name='payment_method',
            new_name='payment_details',
        ),
    ]
