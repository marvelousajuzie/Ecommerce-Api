# Generated by Django 5.0.2 on 2024-05-08 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecomapi', '0012_remove_cart_product_remove_cart_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusers',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecomapi.role'),
        ),
    ]