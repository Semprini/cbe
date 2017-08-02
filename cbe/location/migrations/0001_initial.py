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
            name='City',
            fields=[
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('iso2_code', models.CharField(blank=True, max_length=2)),
                ('iso_numeric', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('x', models.CharField(max_length=30)),
                ('y', models.CharField(max_length=30)),
                ('z', models.CharField(max_length=30)),
                ('geographic_address_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('full_address', models.CharField(blank=True, max_length=250)),
                ('position_number', models.CharField(blank=True, max_length=50)),
                ('type', models.CharField(blank=True, max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PoBoxAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('state_or_province', models.CharField(blank=True, max_length=200)),
                ('box_number', models.CharField(blank=True, max_length=200)),
                ('locality', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RuralPropertyAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('state_or_province', models.CharField(blank=True, max_length=200)),
                ('street_name', models.CharField(blank=True, max_length=200)),
                ('postcode', models.CharField(blank=True, max_length=50)),
                ('locality', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RuralPropertySubAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('state_or_province', models.CharField(blank=True, max_length=200)),
                ('private_street_name', models.CharField(blank=True, max_length=150, null=True)),
                ('sub_unit_number', models.CharField(blank=True, max_length=20, null=True)),
                ('sub_unit_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UrbanPropertyAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('state_or_province', models.CharField(blank=True, max_length=200)),
                ('locality', models.CharField(blank=True, max_length=200)),
                ('postcode', models.CharField(blank=True, max_length=50)),
                ('street_name', models.CharField(blank=True, max_length=200)),
                ('street_number_first', models.IntegerField(blank=True, null=True)),
                ('street_number_first_suffix', models.CharField(blank=True, max_length=20)),
                ('street_number_last', models.IntegerField(blank=True, null=True)),
                ('street_number_last_suffix', models.CharField(blank=True, max_length=20)),
                ('street_suffix', models.CharField(blank=True, max_length=50)),
                ('street_type', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UrbanPropertySubAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('state_or_province', models.CharField(blank=True, max_length=200)),
                ('level_number', models.CharField(blank=True, max_length=20, null=True)),
                ('level_type', models.CharField(blank=True, max_length=50, null=True)),
                ('private_street_name', models.CharField(blank=True, max_length=150, null=True)),
                ('sub_unit_number', models.CharField(blank=True, max_length=20, null=True)),
                ('sub_unit_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
