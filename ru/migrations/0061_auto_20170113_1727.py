# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-13 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0060_auto_20170113_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='orders_complete',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='orders_in_progress',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='orders_new',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]
