from django.contrib import admin
from .models import Category, Product, Sub_Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sub_Category)
