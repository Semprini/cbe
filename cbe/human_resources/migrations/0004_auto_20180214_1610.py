# Generated by Django 2.0.1 on 2018-02-14 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0003_auto_20180131_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identification',
            name='valid_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
