# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-19 00:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0068_auto_20170115_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentdoc',
            name='contact_form_message',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
