# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-08 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funfly', '0003_auto_20160608_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='ninegag',
            name='is_video',
            field=models.BooleanField(default=False),
        ),
    ]
