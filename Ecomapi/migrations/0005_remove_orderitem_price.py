# Generated by Django 5.0.2 on 2024-06-09 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecomapi', '0004_orderitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
    ]