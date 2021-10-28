import re
from django.core import paginator
from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView,FormView,DetailView
from .models import Category, Product, Sub_Category,Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryForm
from django.http import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.utils.http import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core import serializers
from django.http import JsonResponse




# Create your views here.

class MainRedirect(LoginRequiredMixin, View):
    def get(self,request, *args, **kwargs):
        print(self.request.user.user_role)
        if self.request.user.user_role=='Admin':
            return HttpResponseRedirect(reverse('users:admin-dashboard'))

        return HttpResponseRedirect(reverse('products:products'))    


class DashboardClient(LoginRequiredMixin,FormView):
    template_name="dashboard_client.html"
    form_class = CategoryForm
    model = Category


    def get_querylist(self,**kwargs):
         query_list = {
                "product_list":kwargs['product_list'],
                "product":kwargs["product"]
            }
         return query_list

    def get_queryset(self):
        product_list = Product.objects.all()
        page = self.request.GET.get('page',1)
        paginator = Paginator(product_list, 10)
        query_list = {}
        try:
            query_list = self.get_querylist(product_list=product_list, product=paginator.page(page))

        except PageNotAnInteger:
            query_list=self.get_querylist(product_list=product_list, product=paginator.page(1))

        except EmptyPage:
            query_list=self.get_querylist(product_list=product_list, product=paginator.page(paginator.num_pages))

        return query_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("**querlist starts")
        print(self.get_queryset())
        print("**querylist ends")
        context["products"]=self.get_queryset()["product"]
        context["product_list"]=serializers.serialize("json",self.get_queryset()["product_list"])
        print(self.get_queryset())
        return context
    
    def post(self, request, *args, **kwargs):
        category = self.request.POST.get('category')
        sub_category = self.request.POST.get('sub_category')
        query_params = {
            'category':category,
            'sub_category':sub_category
        }   
        return HttpResponseRedirect(reverse_lazy('products:products_api')+f'?{urlencode(query_params)}')
    
    

def ProductCategoryApi(request):
        sub_category = Sub_Category.objects.values_list("category__cat_name","sub_category")
        print(sub_category)
        dct = dict((y,x) for x,y in sub_category)
        lst_dct = {}
        lst_dct['Furniture'] = [k for k, v in dct.items() if v == 'Furniture']
        lst_dct['ElectricAppliances'] = [k for k, v in dct.items() if v == 'ElectricAppliances']
        lst_dct['FitnessEquipment'] = [k for k, v in dct.items() if v == 'FitnessEquipment']
        lst_dct['Crockery'] = [k for k, v in dct.items() if v == 'Crockery']
        return JsonResponse(lst_dct, safe=False)
          
class ProductListFilter(LoginRequiredMixin,ListView):
    template_name="dashboard_client.html"
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
        context =  super().get_context_data(**kwargs)
        context["products"] = self.get_queryset()
        return context
    
class ProductDetailView(LoginRequiredMixin,DetailView):
    template_name="product_detail.html"
    model = Product
    
def get_cart_data(request):
    if request.method == 'POST':
        request_getdata = request.POST.get('data_dict', None)
        request_getdata = json.loads(request_getdata)
        print(type(request_getdata['total_price']))
        cart_obj = Cart.objects.create(user=request.user)
        cart_obj.product_name=request_getdata['prod_name']
        cart_obj.product_category=request_getdata['prod_cat']
        cart_obj.product_subcategory=request_getdata['prod_sub']
        cart_obj.total_price=request_getdata['total_price']
        cart_obj.quantity = request_getdata['quantity']
        cart_obj.save()
        print("data_saved")
        return JsonResponse({'url':reverse('products:get-cart-api')}) 
    
def CartSystem(request):
    cart_obj = Cart.objects.filter(user=request.user)
    context = {
        "orders":cart_obj
    }
    return render(request,"cart.html", context)

## class based view
# class CartSystem(LoginRequiredMixin,ListView):
#     template_name="cart.html"
#     model = Cart
#     context_object_name = "orders"
    
#     def get_queryset(self):
#         query_set = Cart.objects.filter(user=self.request.user)
#         return query_set