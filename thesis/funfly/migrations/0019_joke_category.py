# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funfly', '0018_auto_20160609_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='joke',
            name='category',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
