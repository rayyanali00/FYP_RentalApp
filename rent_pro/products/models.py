from django.db import models
from django.shortcuts import render
from django.urls.base import reverse
from users.models import User
import uuid
from datetime import datetime

# Create your models here.

class Category(models.Model):
    CATEGORY = (
        ("Furniture","Furniture"),
        ("ElectricAppliances","ElectricAppliances"),
        ("FitnessEquipment","FitnessEquipment"),
        ("Crockery","Crockery")        
    )
    cat_name = models.CharField(max_length=255,null=True,blank=True,choices=CATEGORY)
    
    def __str__(self):
        return self.cat_name

class Sub_Category(models.Model):    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="categories")
    sub_category = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.sub_category
    
class Product(models.Model):
    prod_cat = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    prod_sub = models.ForeignKey(Sub_Category, null=True, blank=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_desc = models.CharField(max_length=255, null=False, blank=False)
    prod_img = models.ImageField(upload_to="item_pics", default="nothing.jpg")
    product_price = models.FloatField(max_length=255, null=False, blank=False)
    product_quantity = models.IntegerField(null=False)
    timePeriod = models.IntegerField(null=False)

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=255,null=False, blank=False)
    product_category = models.CharField(max_length=255,null=False, blank=False)
    product_subcategory = models.CharField(max_length=255,null=False, blank=False)
    total_price = models.IntegerField(null=True, blank=True)
    is_checkout = models.BooleanField(default=False)
    quantity = models.IntegerField(null=True)
    
    def __str__(self):
        return self.user.username
    
    
class Order(models.Model):
    ORDER_STATUS = (
        ("pending","Pending"),
        ("delievered","Delievered"),
        ("out for delievery","Out for delievery")
        )
    
    order_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True,auto_now=False)
    deliever_at = models.DateField(null=True, blank=True)
    total_amount = models.FloatField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255,null=True, blank=True, choices=ORDER_STATUS, default="pending")
    
    def __str__(self):
        return str(self.order_id)
    