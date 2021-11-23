import re
from django.core import paginator
from django.db.models import query
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView,FormView,DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Category, Product, Sub_Category,Cart, Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CategoryForm,OrderForm,OrderStatusForm,ProductForm
from django.http import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.utils.http import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CartSerializer, ProductSerializer,OrderSerializer
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

class MainRedirect(LoginRequiredMixin, View):
    def get(self,request, *args, **kwargs):
        print(self.request.user.user_role)
        if self.request.user.user_role=='Admin':
            return HttpResponseRedirect(reverse('users:admin-dashboard'))

        return HttpResponseRedirect(reverse('products:products'))    


class DashboardClient(LoginRequiredMixin,FormView):
    template_name="product/dashboard_client.html"
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
    template_name="product/dashboard_client.html"
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
    template_name="product/product_detail.html"
    model = Product
    
def get_cart_data(request):
    if request.method == 'POST':
        request_getdata = request.POST.get('data_dict', None)
        request_getdata = json.loads(request_getdata)
        cart_obj = Cart.objects.create(user=request.user)
        prod_obj = Product.objects.get(product_name=request_getdata['prod_name'])
        prod_obj.product_quantity = prod_obj.product_quantity - request_getdata['quantity']
        cart_obj.product_name=request_getdata['prod_name']
        cart_obj.product_category=request_getdata['prod_cat']
        cart_obj.product_subcategory=request_getdata['prod_sub']
        cart_obj.total_price=request_getdata['total_price']
        cart_obj.quantity = request_getdata['quantity']
        cart_obj.order_id = "hello"
        cart_obj.save()
        prod_obj.save()
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
        return render(self.request, 'cart/checkout.html', context)
    
    def get_queryset(self,*args,**kwargs):
        qs = Cart.objects.filter(user=self.request.user, is_checkout=False).values('total_price')
        total_price =0
        for i in qs:
            total_price+=i['total_price']
        return total_price

    def get_success_url(self,*args,**kwargs):
        return reverse_lazy('products:order-success')
    
@login_required
def Order_Success(request):
    if request.method == "POST":
        uni_id = uuid.uuid4()
        order_obj = Order.objects.create()
        cart_obj = Cart.objects.filter(user=request.user).update(is_checkout=True,order_id=uni_id)
        order_obj.order_id = uni_id
        order_obj.user = request.user
        order_obj.email = request.POST.get('email')
        order_obj.address = request.POST.get('address')
        order_obj.total_amount = request.POST.get('total_amount')
        order_obj.deliever_at = request.POST.get('deliever_at')
        order_obj.country = request.POST.get('country')
        order_obj.state = request.POST.get('state')
        order_obj.city = request.POST.get('city')
        order_obj.zip_code = request.POST.get('zip_code')
        order_obj.save()

        subject, from_email, to = 'Booking Confirmed', settings.EMAIL_HOST_USER, 'rayyanali929@gmail.com'
        text_content = 'This is an important message.'
        html_content = f'<h1>Confirmation Email</h1> <h2>{request.user} your booking has been confirmed<h2>'\
        f'<a href="http://127.0.0.1:8000/users/order-detail-template/{request.user.id}/{uni_id}"'\
        f'class="btn btn-primary">Check Details</a>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponseRedirect(reverse('products:checkout-success'))
    return Http404
    
@login_required
def CartSystem(request):
    cart_obj = Cart.objects.filter(user=request.user, is_checkout=False)
    cart_obj_count =cart_obj.count()
    context = {
        "orders":cart_obj,
        "count":cart_obj_count
    }
    return render(request,"cart/cart.html", context)

@login_required
def reset_cart(request):
    cart_obj = Cart.objects.filter(user=request.user, is_checkout=False).delete()
    return HttpResponseRedirect(reverse('products:get-cart-api'))

@login_required
def DeleteSingleProduct(request,id):
    cart_obj = Cart.objects.filter(user=request.user, is_checkout=False, id=id).delete()
    return HttpResponseRedirect(reverse('products:get-cart-api'))
    
@login_required
def checkout_success(request):
    order_id_obj = Order.objects.filter(user=request.user).first()
    if order_id_obj.order_id:    
        context = {
            'order_id':order_id_obj.order_id
        }
        return render(request, 'cart/checkout_success.html', context)
    return Http404

@login_required
@api_view(['GET'])
def Order_List(request):
    order_obj = None
    serializer_obj = None
    if request.user.user_role=='Admin':
        order_obj = Order.objects.all()
    else:
        order_obj = Order.objects.filter(user=request.user)    
    serializer_obj = OrderSerializer(order_obj, many=True)
    return Response(serializer_obj.data)

@login_required
def OrderListTemplate(request):
    return render(request, 'orders/orders_list.html')

@login_required
def OrderDetailTemplate(request,pk,order_id):
    context = { 'order_id':order_id,'pk':pk }
    return render(request, 'orders/orders_detail.html',context)

@login_required
@api_view(['GET'])
def OrderDetailApi(request,pk,order_id):
    if request.user.user_role=='Admin':
        cart_obj = Cart.objects.filter(user=pk, is_checkout=True,user__order__status="Pending",user__order__order_id=order_id)
    else:
        cart_obj = Cart.objects.filter(user=request.user, is_checkout=True,user__order__status="Pending",user__order__order_id=order_id)
    serializer_obj = CartSerializer(cart_obj, many=True)
    return Response(serializer_obj.data)

@login_required
def OrderStatusUpdate(request):
    if request.user.user_role == "Admin":
        order_obj = Order.objects.get(order_id=request.GET.get('order_id'))
        form_ins = OrderStatusForm(instance=order_obj)
        context = {
            'form':form_ins,
            'order_id':request.GET.get('order_id')
        }
        return render(request, 'orders/order_status_form.html', context)
    
    raise PermissionDenied()

@login_required
def OrderStatus(request,pk):
    if request.method == "POST":
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('status'),pk)
            order_obj = Order.objects.get(order_id=pk)
            order_obj.status = form.cleaned_data.get('status')
            order_obj.save()
            return HttpResponseRedirect(reverse('products:order-list-template'))

@login_required
@api_view(['GET'])
def products_api(request):
    prod_obj = Product.objects.all()
    serializer_obj = ProductSerializer(prod_obj, many=True)
    return Response(serializer_obj.data)

@login_required
def product_list_template(request):
    if request.user.user_role == "Admin":
        return render(request, 'product/product_list.html')
    raise PermissionDenied()


class CreateProduct(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Product
    template_name = 'product/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products:product-list-template')

    def test_func(self):
        if self.request.user.user_role == "Admin":
            return True
        return False

class UpdateProduct(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    model = Product
    template_name = 'product/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products:product-list-template')
    success_message = 'Product Updated Successfully'

    def test_func(self):
        if self.request.user.user_role == "Admin":
            return True
        return False

def ProductDelete(request,pk):
    prod_obj = Product.objects.get(id=pk).delete()
    messages.success(request,"Product Deleted Successfully")
    return HttpResponseRedirect(reverse('products:product-list-template'))

    
#extra django-rest-framework
#unsued
@api_view(['GET'])
def api_overview(request):
    return Response('Your api-overview')



 