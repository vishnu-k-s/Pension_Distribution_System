# Generated by Django 3.2.10 on 2022-01-10 05:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pension_user_dashboard', '0009_employeservicestatus'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmployeServiceStatus',
            new_name='UserServiceStatus',
        ),
    ]
