# Generated by Django 5.0.2 on 2024-05-11 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecomapi', '0017_cartitems_subtotal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='product',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Ecomapi.product'),
            preserve_default=False,
        ),
    ]