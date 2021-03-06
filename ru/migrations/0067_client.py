# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-13 20:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ru', '0066_auto_20170113_2245'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tel', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50)),
                ('date_birth', models.CharField(blank=True, max_length=15, null=True)),
                ('registered', models.DateTimeField(auto_now_add=True, null=True)),
                ('changed', models.DateTimeField(auto_now=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='D:\\projects\\trans/static/photo')),
                ('init_password', models.CharField(blank=True, max_length=50, null=True)),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_changed_by', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_creator', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
