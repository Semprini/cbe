# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-28 11:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplier_partner', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buyer',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ['id']},
        ),
    ]
