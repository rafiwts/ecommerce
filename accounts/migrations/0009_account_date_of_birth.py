# Generated by Django 4.2.6 on 2023-12-04 13:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0008_rename_account_account_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True, verbose_name="Birth date"),
        ),
    ]
