# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-28 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whats_on_dot_com', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='event',
            name='slug',
        ),
        migrations.AddField(
            model_name='event',
            name='event_picture',
            field=models.ImageField(blank=True, upload_to='event_images/'),
        ),
        migrations.AddField(
            model_name='event',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='number_followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='forename',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_images'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='surname',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='event',
            name='interested',
            field=models.ManyToManyField(blank=True, related_name='interested', to='whats_on_dot_com.UserProfile'),
        ),
    ]
