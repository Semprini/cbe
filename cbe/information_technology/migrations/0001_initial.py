# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-02 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('documentation', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ComponentClassification',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('documentation', models.TextField(blank=True)),
            ],
        ),
    ]
