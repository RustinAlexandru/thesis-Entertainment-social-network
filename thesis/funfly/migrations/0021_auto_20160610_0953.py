# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-10 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funfly', '0020_joke_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joke',
            name='identifier',
            field=models.CharField(db_index=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='ninegag',
            name='title',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
