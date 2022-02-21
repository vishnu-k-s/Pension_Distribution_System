# Generated by Django 3.2.10 on 2022-01-10 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pension_user_dashboard', '0010_rename_employeservicestatus_userservicestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userservicestatus',
            name='service_status',
            field=models.CharField(choices=[('Active', 'Active'), ('Retried', 'Retried')], default=None, max_length=10),
        ),
    ]
