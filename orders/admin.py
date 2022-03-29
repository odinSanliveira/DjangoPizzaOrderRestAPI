from django.contrib import admin
from .models import Order
# Register your models here.


@admin.register(Order)
class OrderAAdmin(admin.ModelAdmin):
    list_display=['id','size', 'flavour', 'order_status', 'quantity', 'created_at', 'customer']
    list_filter=['created_at', 'order_status', 'size', 'customer']


