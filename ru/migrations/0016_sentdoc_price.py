# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-04 22:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0015_sentfiles_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentdoc',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
