# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-22 14:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ru', '0074_sentdoc_translation_downloaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCommentsClients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('author_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ru.Role')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ru.SentDoc')),
            ],
        ),
    ]
