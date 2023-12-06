# Generated by Django 4.2.6 on 2023-12-05 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0013_remove_accounttype_account_account_account_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="accounts.accounttype",
            ),
        ),
        migrations.AlterField(
            model_name="useraddress",
            name="account",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="address",
                to="accounts.account",
            ),
        ),
    ]