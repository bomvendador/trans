# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-11 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0045_sentdoc_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentdoc',
            name='translation_sent_date',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
