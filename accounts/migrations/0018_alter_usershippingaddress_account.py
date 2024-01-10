# Generated by Django 4.2.6 on 2024-01-08 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0017_alter_accounttype_table_usershippingaddress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usershippingaddress",
            name="account",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shipping_addresses",
                to="accounts.account",
            ),
        ),
    ]