# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-07 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_address_orderaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='a_using',
            field=models.BooleanField(default=False),
        ),
    ]