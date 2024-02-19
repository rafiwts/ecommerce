# Generated by Django 4.2.6 on 2024-02-19 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0026_alter_resetpasswordlink_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resetpasswordlink",
            name="expiration_time",
            field=models.IntegerField(
                blank=True, db_column="expiration time [s]", default=86400, null=True
            ),
        ),
    ]