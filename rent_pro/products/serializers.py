from rest_framework import serializers
from .models import Cart, Product,Order, Category,Sub_Category




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class Sub_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_Category
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","product_name","product_price","product_quantity","prod_cat","prod_sub"]        
        
        
    def to_representation(self, instance):
        '''
        replace the prod_cat,prod_sub ids with the actual category and subcategory names
        '''
        rep = super().to_representation(instance)
        obj = CategorySerializer(instance.prod_cat).data
        obj = obj.get("cat_name")
        obj1 = Sub_CategorySerializer(instance.prod_sub).data
        obj1 = obj1.get("sub_category")
        rep['prod_cat'] = obj
        rep['prod_sub'] = obj1
        return rep
            
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        
class OrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id','email','ordered_at','total_amount','your_bid_total','user']
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ('user','is_checkout')
        
class OrderGraphSerializer(serializers.ModelSerializer):
    counted = serializers.IntegerField()
    dated = serializers.CharField()
    class Meta:
        model = Order
        fields = ['id','ordered_at','counted','dated',]