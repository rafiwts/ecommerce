# Generated by Django 4.2.6 on 2023-12-04 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_alter_account_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="address",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.useraddress",
            ),
        ),
    ]
