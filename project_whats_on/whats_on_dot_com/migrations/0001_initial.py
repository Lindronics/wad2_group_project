# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-02-27 16:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('date_time', models.DateTimeField()),
                ('slug', models.SlugField(unique=True)),
                ('location_info', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=1024)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whats_on_dot_com.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('follows', models.ManyToManyField(blank=True, related_name='_userprofile_follows_+', to='whats_on_dot_com.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ManyToManyField(related_name='host', to='whats_on_dot_com.UserProfile'),
        ),
        migrations.AddField(
            model_name='event',
            name='interested',
            field=models.ManyToManyField(related_name='interested', to='whats_on_dot_com.UserProfile'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, to='whats_on_dot_com.Tag'),
        ),
    ]
