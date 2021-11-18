from rest_framework import serializers
from .models import Cart, Product,Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"