# Generated by Django 3.2.10 on 2021-12-29 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pension_user_authentication', '0007_alter_useraccount_email_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='email_id',
            field=models.EmailField(max_length=251, unique=True),
        ),
    ]