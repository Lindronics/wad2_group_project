# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-12 21:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_on_dot_com', '0006_merge_20180307_1010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='longtitude',
            new_name='longitude',
        ),
    ]