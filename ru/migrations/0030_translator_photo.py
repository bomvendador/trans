# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-06 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0029_auto_20170106_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='translator',
            name='photo',
            field=models.ImageField(null=True, upload_to='D:\\projects\\trans/static/photo'),
        ),
    ]
