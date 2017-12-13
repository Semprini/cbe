# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-14 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_limit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('credit_status', models.CharField(choices=[('active', 'active'), ('stop', 'stop')], max_length=100)),
                ('credit_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('transaction_limit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CreditAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_type', models.CharField(choices=[('risk', 'risk'), ('threshold', 'threshold'), ('breech', 'breech'), ('other', 'other')], max_length=300)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CreditBalanceEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CreditProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('credit_risk_rating', models.IntegerField(blank=True, null=True)),
                ('credit_score', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
