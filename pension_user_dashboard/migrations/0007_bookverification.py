# Generated by Django 3.2.10 on 2022-01-07 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pension_user_dashboard', '0006_alter_userprofile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(max_length=8)),
                ('Slot_time', models.CharField(max_length=8)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]