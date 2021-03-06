# Generated by Django 2.0.1 on 2018-02-15 09:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('supplier_partner', '0002_auto_20180214_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='valid_from',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='valid_from',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='valid_from',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
