# Generated by Django 4.1.5 on 2023-02-07 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_remove_order_data_order_detail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_detail',
            name='order_id',
        ),
        migrations.AddField(
            model_name='order_detail',
            name='order_id_ref',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.order_data'),
        ),
    ]
