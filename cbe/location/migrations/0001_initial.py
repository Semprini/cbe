# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 11:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbsoluteLocalLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('geographic_address_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('full_address', models.CharField(blank=True, max_length=250)),
                ('position_number', models.CharField(blank=True, max_length=50)),
                ('type', models.CharField(blank=True, max_length=150)),
                ('name', models.CharField(max_length=200)),
                ('x', models.CharField(max_length=30)),
                ('y', models.CharField(max_length=30)),
                ('z', models.CharField(max_length=30)),
                ('geographic_address_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_absolutelocallocation_ownership', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
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
            name='PoBoxAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('state_or_province', models.CharField(blank=True, max_length=200)),
                ('box_number', models.CharField(blank=True, max_length=200)),
                ('locality', models.CharField(blank=True, max_length=200)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Country')),
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
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Country')),
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
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Country')),
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
                ('building_name', models.CharField(blank=True, max_length=200, null=True)),
                ('level_number', models.CharField(blank=True, max_length=20, null=True)),
                ('level_type', models.CharField(blank=True, max_length=50, null=True)),
                ('private_street_name', models.CharField(blank=True, max_length=150, null=True)),
                ('sub_unit_number', models.CharField(blank=True, max_length=20, null=True)),
                ('sub_unit_type', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Country')),
                ('urban_property_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.UrbanPropertyAddress')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Country'),
        ),
    ]
