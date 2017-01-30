# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-10 19:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ru', '0042_translator_init_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='translator',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
