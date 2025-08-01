# Generated by Django 5.2.3 on 2025-07-16 21:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0006_company_custom_sms_provider_company_sms_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='custom_sms_provider',
        ),
        migrations.RemoveField(
            model_name='company',
            name='sms_address',
        ),
        migrations.RemoveField(
            model_name='company',
            name='sms_password',
        ),
        migrations.RemoveField(
            model_name='company',
            name='sms_token',
        ),
        migrations.RemoveField(
            model_name='company',
            name='sms_user',
        ),
        migrations.AddField(
            model_name='company',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('deactivated', 'Deactivated')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='service_expiration',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insurance.company'),
        ),
    ]
