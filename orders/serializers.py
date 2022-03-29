from .models import Order
from rest_framework import serializers


class OrderCreationSerializer(serializers.ModelSerializer):
    order_status = serializers.HiddenField(default='PENDING')
    size = serializers.CharField(max_length=20)
    quantity = serializers.IntegerField(default=1)
    flavour=serializers.CharField(max_length=40)


    class Meta:
        model = Order
        fields = ['order_status', 'size', 'quantity','flavour']
    
class OrderDetailSerializer(serializers.ModelSerializer):
    
    order_status = serializers.CharField(default='PENDING')
    size = serializers.CharField(max_length=20)
    flavour=serializers.CharField(max_length=40)
    quantity = serializers.IntegerField(default=1)
    created_at = serializers.DateTimeField()
    update_at=serializers.DateTimeField()

    class Meta:
        model = Order
        fields = ['id', 'size', 'flavour', 'order_status', 'quantity', 'created_at', 'update_at']
    

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    order_status = serializers.CharField(default='PENDING')

    class Meta:
        model=Order
        fields=['order_status']
