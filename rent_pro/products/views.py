import re
from django.core import paginator
from django.db.models import query
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView,FormView,DetailView
from .models import Category, Product, Sub_Category,Cart, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryForm,OrderForm
from django.http import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.utils.http import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CartSerializer, ProductSerializer,OrderSerializer
from django.core.exceptions import PermissionDenied
from django.db.models import Q

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
    
class OrderView(LoginRequiredMixin,View):
    form_class = OrderForm
    model = Order
    
    def get(self, *args, **kwargs):
        context = {
            'form':self.form_class,
            'total_amount':self.get_queryset(),
            'success_url':self.get_success_url()
        }
        return render(self.request, 'checkout.html', context)
    
    def get_queryset(self,*args,**kwargs):
        qs = Cart.objects.filter(user=self.request.user, is_checkout=False).values('total_price')
        total_price =0
        for i in qs:
            total_price+=i['total_price']
        return total_price

    def get_success_url(self,*args,**kwargs):
        return reverse_lazy('products:order-success')
    
    
def Order_Success(request):
    if request.method == "POST":
        order_obj = Order.objects.create()
        cart_obj = Cart.objects.filter(user=request.user).update(is_checkout=True)
        order_obj.user = request.user
        order_obj.email = request.POST.get('email')
        order_obj.address = request.POST.get('address')
        order_obj.total_amount = request.POST.get('total_amount')
        order_obj.deliever_at = request.POST.get('deliever_at')
        order_obj.save()
        subject = 'welcome to GFG world'
        message = f'Hi {request.user.username}, thank you for registering in geeksforgeeks.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['rayyan@inqline.com', ]
        send_mail( subject, message, email_from, recipient_list )

        return HttpResponseRedirect(reverse('products:checkout-success'))
    return Http404
    
def CartSystem(request):
    cart_obj = Cart.objects.filter(user=request.user, is_checkout=False)
    cart_obj_count =cart_obj.count()
    context = {
        "orders":cart_obj,
        "count":cart_obj_count
    }
    return render(request,"cart.html", context)

def reset_cart(request):
    cart_obj = Cart.objects.filter(user=request.user, is_checkout=False).delete()
    return HttpResponseRedirect(reverse('products:get-cart-api'))

def DeleteSingleProduct(request,id):
    cart_obj = Cart.objects.filter(user=request.user, is_checkout=False, id=id).delete()
    return HttpResponseRedirect(reverse('products:get-cart-api'))
    
def checkout_success(request):
    order_id_obj = Order.objects.filter(user=request.user).first()
    if order_id_obj.order_id:    
        context = {
            'order_id':order_id_obj.order_id
        }
        return render(request, 'checkout_success.html', context)
    return Http404

@api_view(['GET'])
def Order_List(request):
    order_obj = Order.objects.all()
    serializer_obj = OrderSerializer(order_obj, many=True)
    return Response(serializer_obj.data)

def OrderListTemplate(request):
    if request.user.user_role == 'Admin':
        return render(request, 'orders_list.html')
    raise PermissionDenied()

@api_view(['GET'])
def OrderDetailView(request,pk):
    cart_obj = Cart.objects.filter(user=pk, is_checkout=True)
    serializer_obj = CartSerializer(cart_obj, many=True)
    return Response(serializer_obj.data)

##extra django-rest-framework
@api_view(['GET'])
def api_overview(request):
    return Response('Your api-overview')

@api_view(['GET'])
def products_api(request,pk):
    prod_obj = Product.objects.get(id=pk)
    serializer_obj = ProductSerializer(prod_obj, many=False)
    return Response(serializer_obj.data)

 