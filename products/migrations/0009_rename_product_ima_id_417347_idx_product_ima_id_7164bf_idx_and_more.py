# Generated by Django 4.2.6 on 2024-06-12 21:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_alter_productimage_options"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="productimage",
            new_name="product_ima_id_7164bf_idx",
            old_name="product_ima_id_417347_idx",
        ),
        migrations.AlterModelTable(
            name="productimage",
            table="product_image",
        ),
    ]
