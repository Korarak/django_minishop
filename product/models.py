from django.db import models

# Create your models here.
class product_data(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, null=True)
    product_qty = models.IntegerField(null=True)
    product_price = models.IntegerField(null=True)
    product_detail =models.TextField(null=True)

class order_data(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_detail = models.CharField(max_length=100,null=True)
    order_date = models.DateField(null=True)
    order_address = models.CharField(max_length=200,null=True)
    order_tel = models.CharField(max_length=11,null=True)
    order_username = models.CharField(max_length=100,null=True)
    order_email = models.EmailField(max_length=100,null=True)

class order_detail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    p_id = models.CharField(max_length=10,null=True)
    p_qty = models.IntegerField(null=True)
    p_price = models.IntegerField(null=True)

class cart_add(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=100,null=True)
    product_qty = models.IntegerField(null=True)
    product_price = models.IntegerField(null=True)
    email = models.EmailField(max_length=100,null=True)