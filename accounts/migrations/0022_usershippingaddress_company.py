# Generated by Django 4.2.6 on 2024-02-04 20:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0021_usershippingaddress_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usershippingaddress",
            name="company",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
