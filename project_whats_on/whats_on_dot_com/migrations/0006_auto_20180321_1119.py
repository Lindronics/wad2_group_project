# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-03-21 11:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_on_dot_com', '0005_auto_20180319_2027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='longtitude',
            new_name='longitude',
        ),
    ]