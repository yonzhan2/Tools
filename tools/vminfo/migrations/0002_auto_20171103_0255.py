# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-03 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vminfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vmlist',
            name='vmip',
            field=models.CharField(default='N/A', max_length=16),
        ),
    ]
