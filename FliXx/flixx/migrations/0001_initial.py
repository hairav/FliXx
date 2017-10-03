# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Username', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=100)),
                ('DateOfBirth', models.DateField()),
                ('Password', models.CharField(max_length=15)),
                ('Headshot', models.ImageField(upload_to=b'photos/%Y/%h/%d/%H/%M/%S')),
                ('IsLoggedIn', models.BinaryField(default=0)),
            ],
        ),
    ]
