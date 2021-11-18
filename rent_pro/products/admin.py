from django.contrib import admin
from .models import Category, Product, Sub_Category,Cart, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('ordered_at',)

admin.site.register(Order, OrderAdmin)