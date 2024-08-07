# Generated by Django 4.2.6 on 2024-07-29 18:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0013_alter_product_for_sale_favoriteproduct"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favoriteproduct",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite_products",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
