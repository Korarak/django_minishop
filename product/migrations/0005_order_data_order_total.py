# Generated by Django 4.1.5 on 2023-02-04 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_cart_add_product_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_data',
            name='order_total',
            field=models.IntegerField(null=True),
        ),
    ]