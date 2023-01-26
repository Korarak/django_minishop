from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(product_data)
admin.site.register(order_data)
admin.site.register(order_detail)
admin.site.register(cart_add)