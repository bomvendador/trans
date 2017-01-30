# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-12 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0049_auto_20170112_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentdoc',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='sentdoc',
            name='tel',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='sentdoc',
            name='text',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
