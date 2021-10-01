from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView
from .models import Product

# Create your views here.
class DashboardClient(ListView):
    template_name="dashboard_client.html"

    def get_queryset(self):
        product = Product.objects.filter(prod_cat__cat_name__contains="Furniture",prod_sub__sub_category__contains="Bed")
        print(product)        
        return product
    
class ProductListFilter(ListView):
    def get_queryset(self):
        if self.request.method=="GET":
            query_set = {}
            cat = self.request.GET.get('category',None)
            sub_cat = self.request.GET.get('sub_category',None)
            
            if cat is not None and sub_cat is not None:
                query_set = Product.objects.filter(prod_cat__cat_name__contains=cat,prod_sub__sub_category__contains=sub_cat)
                return query_set
        return query_set
    
    def get_context_data(self, **kwargs):
        print(self.get_queryset())
        