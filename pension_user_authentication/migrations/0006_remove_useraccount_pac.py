# Generated by Django 3.2.10 on 2021-12-28 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pension_user_authentication', '0005_useraccount_pac'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='pac',
        ),
    ]