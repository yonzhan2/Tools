# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vminfo', '0002_auto_20171103_0255'),
    ]

    operations = [
        migrations.CreateModel(
            name='VCInfo',
            fields=[
                ('vcdns', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('vcname', models.CharField(max_length=32)),
            ],
        ),
    ]
