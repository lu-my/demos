# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-27 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_foodtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodtype',
            name='childtypenames',
            field=models.CharField(max_length=255),
        ),
    ]
