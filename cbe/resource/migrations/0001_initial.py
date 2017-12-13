# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-14 12:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import gm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('party', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogicalResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_state', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Owner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhysicalResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_state', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True)),
                ('power_state', models.CharField(blank=True, choices=[('on', 'on'), ('off', 'off'), ('starting', 'starting'), ('stopping', 'stopping')], max_length=100, null=True)),
                ('place_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Owner')),
                ('physical_objects', gm2m.fields.GM2MField(related_name='objects', through_fields=('gm2m_src', 'gm2m_tgt', 'gm2m_ct', 'gm2m_pk'))),
                ('place_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resource_physicalresource_ownership', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResourceOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('interaction_status', models.CharField(blank=True, max_length=100, null=True)),
                ('place_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('place_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resource_resourceorder_place_ownership', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResourceOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_interaction_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('action', models.CharField(blank=True, choices=[('add', 'add'), ('update', 'update'), ('delete', 'delete')], max_length=50, null=True)),
                ('place_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('business_interaction_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resource_resourceorderitem_interaction_ownership', to='contenttypes.ContentType')),
                ('place_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resource_resourceorderitem_ownership', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
