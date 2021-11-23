from django.contrib import admin
from .models import Category, Product, Sub_Category,Cart, Order

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    ...
    search_fields = ['product_name',]

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('ordered_at',)
    


admin.site.register(Order, OrderAdmin)