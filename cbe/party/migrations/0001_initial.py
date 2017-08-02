# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-02 11:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('party_role_object_id', models.PositiveIntegerField(null=True)),
                ('email_address', models.EmailField(max_length=200)),
                ('party_role_content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericPartyRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(blank=True, choices=[('Undisclosed', 'Undisclosed'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50, null=True)),
                ('family_names', models.CharField(blank=True, max_length=200)),
                ('given_names', models.CharField(blank=True, max_length=200)),
                ('middle_names', models.CharField(blank=True, max_length=200)),
                ('form_of_address', models.CharField(blank=True, max_length=100)),
                ('legal_name', models.CharField(blank=True, max_length=200)),
                ('marital_status', models.CharField(blank=True, choices=[('Undisclosed', 'Undisclosed'), ('Single', 'Single'), ('Married', 'Married'), ('Other', 'Other')], max_length=100, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=200)),
                ('nationality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Country')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('organisation_type', models.CharField(blank=True, max_length=200, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_organisations', to='party.Organisation')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Individual')),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Organisation')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PartyRoleAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('association_type', models.CharField(max_length=200)),
                ('association_from_object_id', models.CharField(max_length=200)),
                ('association_to_object_id', models.CharField(max_length=200)),
                ('association_from_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='party_partyroleassociation_from', to='contenttypes.ContentType')),
                ('association_to_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='party_partyroleassociation_to', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PhysicalContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('party_role_object_id', models.PositiveIntegerField(null=True)),
                ('address_object_id', models.PositiveIntegerField()),
                ('address_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='party_physicalcontact_address_ownership', to='contenttypes.ContentType')),
                ('party_role_content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TelephoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('party_role_object_id', models.PositiveIntegerField(null=True)),
                ('number', models.CharField(max_length=50)),
                ('party_role_content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='individual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Individual'),
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Organisation'),
        ),
    ]
