# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_algorithm_filepath'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='general_description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
