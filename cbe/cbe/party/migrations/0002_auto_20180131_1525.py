# Generated by Django 2.0.1 on 2018-01-31 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resource', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('party', '0001_initial'),
        ('location', '0002_auto_20180131_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='logical_resources',
            field=models.ManyToManyField(blank=True, related_name='party_owner_logical_resources', to='resource.LogicalResource'),
        ),
        migrations.AddField(
            model_name='owner',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Organisation'),
        ),
        migrations.AddField(
            model_name='owner',
            name='physical_contacts',
            field=models.ManyToManyField(blank=True, related_name='party_owner_physical_contacts', to='party.PhysicalContact'),
        ),
        migrations.AddField(
            model_name='owner',
            name='physical_resources',
            field=models.ManyToManyField(blank=True, related_name='party_owner_physical_resources', to='resource.PhysicalResource'),
        ),
        migrations.AddField(
            model_name='owner',
            name='telephone_numbers',
            field=models.ManyToManyField(blank=True, related_name='party_owner_telephone_numbers', to='party.TelephoneNumber'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_organisations', to='party.Organisation'),
        ),
        migrations.AddField(
            model_name='individual',
            name='nationality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Country'),
        ),
        migrations.AddField(
            model_name='individual',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='email_contacts',
            field=models.ManyToManyField(blank=True, related_name='party_genericpartyrole_email_contacts', to='party.EmailContact'),
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='individual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Individual'),
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='logical_resources',
            field=models.ManyToManyField(blank=True, related_name='party_genericpartyrole_logical_resources', to='resource.LogicalResource'),
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Organisation'),
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='physical_contacts',
            field=models.ManyToManyField(blank=True, related_name='party_genericpartyrole_physical_contacts', to='party.PhysicalContact'),
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='physical_resources',
            field=models.ManyToManyField(blank=True, related_name='party_genericpartyrole_physical_resources', to='resource.PhysicalResource'),
        ),
        migrations.AddField(
            model_name='genericpartyrole',
            name='telephone_numbers',
            field=models.ManyToManyField(blank=True, related_name='party_genericpartyrole_telephone_numbers', to='party.TelephoneNumber'),
        ),
    ]