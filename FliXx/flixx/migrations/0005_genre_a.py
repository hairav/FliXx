# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-30 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flixx', '0004_auto_20170930_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='a',
            field=models.ManyToManyField(to='flixx.user'),
        ),
    ]