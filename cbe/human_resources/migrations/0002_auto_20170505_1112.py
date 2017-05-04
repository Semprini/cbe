# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 11:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import gm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('party', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('human_resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Organisation'),
        ),
        migrations.AddField(
            model_name='staff',
            name='contact_mediums',
            field=gm2m.fields.GM2MField(through_fields=('gm2m_src', 'gm2m_tgt', 'gm2m_ct', 'gm2m_pk')),
        ),
        migrations.AddField(
            model_name='staff',
            name='party_content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='human_resources_staff_ownership', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='identification',
            name='identification_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human_resources.IdentificationType'),
        ),
        migrations.AddField(
            model_name='identification',
            name='party_content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='human_resources_identification_ownership', to='contenttypes.ContentType'),
        ),
    ]
