# Generated by Django 4.2.6 on 2023-12-03 21:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_useraddress_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="account",
        ),
        migrations.AddField(
            model_name="account",
            name="account",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="account",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]