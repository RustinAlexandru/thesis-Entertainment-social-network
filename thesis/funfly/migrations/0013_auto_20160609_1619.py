# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funfly', '0012_auto_20160609_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joke',
            name='joke_category',
        ),
        migrations.AddField(
            model_name='joke',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
