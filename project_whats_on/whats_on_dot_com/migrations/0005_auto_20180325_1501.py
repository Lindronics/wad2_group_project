# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-25 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whats_on_dot_com', '0004_auto_20180325_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_picture',
            field=models.ImageField(blank=True, upload_to=b'event_images'),
        ),
    ]
