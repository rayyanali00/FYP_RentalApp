import re
from django.core import paginator
from django.db.models import query
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView,FormView,DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Category, Product, Sub_Category,Cart, Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CategoryForm,OrderForm,OrderStatusForm,ProductForm,OrderStatusForm,OrderDelieveryStatusForm
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
from .serializers import CartSerializer, OrderGraphSerializer, ProductSerializer,OrderSerializer,OrderRequestSerializer
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from notifications.signals import notify
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from django.db.models.functions import Cast, Trunc
from django.db.models import (Q, 
                            Sum, 
                            F, 
                            Max, 
                            Min,
                            Count,
                            Value,
                            ExpressionWrapper, 
                            DurationField,
                            DecimalField, 
                            DateField,
                            DateTimeField, 
                            TimeField)

# Create your views here.
User = get_user_model()
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
        # lst_dct['Furniture'] = [k for k, v in dct.items() if v == 'Furniture']
        # lst_dct['ElectricAppliances'] = [k for k, v in dct.items() if v == 'ElectricAppliances']
        # lst_dct['FitnessEquipment'] = [k for k, v in dct.items() if v == 'FitnessEquipment']
        # lst_dct['Crockery'] = [k for k, v in dct.items() if v == 'Crockery']
        for k,v in dct.items():
            lst_dct[v] = [i for i,j in dct.items() if j == v]
        print(lst_dct)
        print("****************")
        print(dct)
        print("****************")
        print(lst_dct['Furniture'])
        
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
        print()
        cart_obj = Cart.objects.create(user=request.user)
        prod_obj = Product.objects.get(product_name=request_getdata['prod_name'])
        prod_obj.product_quantity = prod_obj.product_quantity - request_getdata['quantity']
        return_date = (datetime.now() + timedelta(days=request_getdata['days']+1)).strftime('%Y-%m-%d')
        cart_obj.product_name=request_getdata['prod_name']
        cart_obj.product_category=request_getdata['prod_cat']
        cart_obj.product_subcategory=request_getdata['prod_sub']
        cart_obj.total_price=request_getdata['total_price']
        cart_obj.quantity = request_getdata['quantity']
        cart_obj.your_bid_price = request_getdata['your_bid_price']
        cart_obj.order_id = "hello"
        cart_obj.return_date = return_date
        
        cart_obj.save()
        prod_obj.save()
        return JsonResponse({'url':reverse('products:get-cart-api')})
    
class OrderView(LoginRequiredMixin,View):
    form_class = OrderForm
    model = Order
    
    def get(self, *args, **kwargs):
        context = {
            'form':self.form_class,
            'total_amount':self.get_queryset()['total_price'],
            'total_bid_price':self.get_queryset()['total_bid_price'],
            'success_url':self.get_success_url()
        }
        return render(self.request, 'cart/checkout.html', context)
    
    def get_queryset(self,*args,**kwargs):
        qs = Cart.objects.filter(user=self.request.user, is_checkout=False).values('total_price','your_bid_price')
        context = {
        "total_price":0,
        "total_bid_price" :0
        }
        print(qs)
        for i in qs:
            context['total_price']+=i['total_price']
            context['total_bid_price']+=i['your_bid_price']
        return context

    def get_success_url(self,*args,**kwargs):
        return reverse_lazy('products:order-success')
    
@login_required
def Order_Success(request):
    if request.method == "POST":
        uni_id = uuid.uuid4()
        order_obj = Order.objects.create()
        print(uni_id)
        cart_obj = Cart.objects.filter(user=request.user,is_checkout=False).update(is_checkout=True,order_id=uni_id)
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
        order_obj.your_bid_total = request.POST.get('your_bid_total')
        order_obj.save()
        user_obj = User.objects.get(user_role='Admin')
        print(user_obj)
        notify.send(request.user, recipient=user_obj, verb='Notification', description=f'Order Request from {request.user.email}')

        subject, from_email, to = 'Booking Request', settings.EMAIL_HOST_USER, request.user.email
        text_content = ''
        html_content = f'<h1>Booking Request Email</h1> <h2>{request.user} Your booking request has been sent<h2>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        subject, from_email, to = 'New Booking Request', settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER
        text_content = ''
        html_content = f'<h1>Booking Request Email</h1> <h2>You have received Booking Request from {request.POST.get("email")}<h2> <p><b>Order Id : </b>{uni_id}<p>'
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
    order_id_obj = Order.objects.filter(user=request.user).last()
    print(order_id_obj.order_id)
    context = {
        'order_id':order_id_obj.order_id
    }
    print(context)
    return render(request, 'cart/checkout_success.html', context)

@login_required
@api_view(['GET'])
def Order_List(request):
    order_obj = None
    serializer_obj = None
    if request.user.user_role=='Admin':
        order_obj = Order.objects.filter(is_accepted='Accept')
    else:
        order_obj = Order.objects.filter(user=request.user, is_accepted='Accept')    
    serializer_obj = OrderSerializer(order_obj, many=True)
    return Response(serializer_obj.data)

@login_required
@api_view(['GET'])
def PendingOrderApi(request):
    order_obj = Order.objects.filter(status='Pending', payment_process="Received")
    serializer_obj = OrderSerializer(order_obj, many=True)
    return Response(serializer_obj.data)

@login_required
@api_view(['GET'])
def DelieveredOrderApi(request):
    order_obj = Order.objects.filter(status='Delievered', payment_process="Received")
    serializer_obj = OrderSerializer(order_obj, many=True)
    return Response(serializer_obj.data)


@login_required
def OrderListTemplate(request):
    return render(request, 'orders/orders_list.html')

@login_required
def PendingOrderListTemplate(request):
    return render(request, 'orders/pending-orders-list.html')

@login_required
def DelieveredOrderListTemplate(request):
    return render(request, 'orders/delievered-orders-list.html')


@login_required
@api_view(['GET'])
def Order_Request(request):
    if request.user.user_role == "General":
        order_obj = Order.objects.filter(user=request.user,is_accepted='Pending')
    else:
        order_obj = Order.objects.filter(is_accepted='Pending')
    serializer_obj = OrderRequestSerializer(order_obj, many=True)
    return Response(serializer_obj.data)


@login_required
def OrderRequestTemplate(request):
    return render(request, 'orders/order_requests_list.html')

@login_required
def OrderRequestForm(request):
    context = {
        "form":OrderStatusForm(),
        "order_id":request.GET.get('order_id'),
        "email":request.GET.get('email')
    }
    return render(request,'orders/order_request_form.html',context)

@login_required
def SendReturnEmailList(request):
    if request.user.user_role == 'Admin':
        return render(request,'return_items/send_return_email.html')
    return Http404


@login_required
@api_view(['GET'])
def ItemListApi(request):
    dt_diff = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    cart_obj = Cart.objects.filter(return_date__lte=dt_diff, return_email_sent=False)
    serializer_obj = CartSerializer(cart_obj, many=True)
    return Response(serializer_obj.data)

def SendEmailForm(request):
    if request.user.user_role == "Admin":
        qs = Cart.objects.filter(order_id=request.GET.get('order_id')).values('user__email')
        print(qs)
        context = dict(
                {
            'id':request.GET.get('id'),
            'order_id':request.GET.get('order_id'),
            'product_category':request.GET.get('product_cat'),
            'product_sub_category':request.GET.get('product_sub'),
            'title':request.GET.get('title'),
            'email':qs[0]['user__email']
            }
            )
        return render(request,'return_items/send_email_form.html', context=context)
    return Http404

def SendReturnEmail(request):
    if request.method == 'POST':
        print(request.POST)
        subject, from_email, to = 'Item Return!!! 3 days left', settings.EMAIL_HOST_USER, request.POST.get('email')
        text_content = f"Dear Customer\
            It's Time to return our item, I hope you enjoyed our service\
                Item Title:{request.POST.get('title')} Order ID is {request.POST.get('order_id')}\
                    \n Hopefully, we can assis you in future for your needs"
        # html_content = f'<h1>Order Accepted</h1> <h2>Your order request has been accepted<h2> <h3>Order Id : {request.POST.get("order_id")}</h3> <h3>Please complete your payment details, so we can deliever your order at your door step</h3><h5>Here is the link for payment process</h5>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(text_content, "text/html")
        msg.send()
        print(request.POST.get('id'))
        qs = Cart.objects.filter(id=request.POST.get('product_id')).update(return_email_sent=True)
        return HttpResponseRedirect(reverse('products:send-return-email'))

def OrderRequestStatus(request):
    if request.method == "POST":
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            order_obj = Order.objects.filter(order_id=request.POST.get('order_id')).update(is_accepted=form.cleaned_data.get('is_accepted'))
            if form.cleaned_data.get('is_accepted') == "Accept":
                subject, from_email, to = 'Order Accepted', settings.EMAIL_HOST_USER, request.POST.get('email')
                text_content = ''
                html_content = f'<h1>Order Accepted</h1> <h2>Your order request has been accepted<h2> <h3>Order Id : {request.POST.get("order_id")}</h3> <h3>Please complete your payment details, so we can deliever your order at your door step</h3><h5>Here is the link for payment process</h5>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            else:
                subject, from_email, to = 'Order Rejected', settings.EMAIL_HOST_USER, request.POST.get('email')
                text_content = ''
                html_content = f'<h1>Order Accepted</h1> <h2>Unfortunately, we can not accept your order, since your bid price is low<h2> <h3>Order Id : {request.POST.get("order_id")}</h3> <h3>You can place your order by placing another bid</h3>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            return HttpResponseRedirect(reverse_lazy('products:order-request-template'))
        return HttpResponseBadRequest
    
@login_required
def OrderDetailTemplate(request,pk,order_id):
    context = { 'order_id':order_id,'pk':pk }
    return render(request, 'orders/orders_detail.html',context)

@login_required
@api_view(['GET'])
def OrderDetailApi(request,pk,order_id):
    if request.user.user_role=='Admin':
        cart_obj = Cart.objects.filter(user=pk, is_checkout=True,order_id=order_id)
    else:
        cart_obj = Cart.objects.filter(user=request.user, is_checkout=True,order_id=order_id)
    serializer_obj = CartSerializer(cart_obj, many=True)
    return Response(serializer_obj.data)


@login_required
def OrderStatusUpdate(request):
    if request.user.user_role == "Admin":
        order_obj = Order.objects.get(order_id=request.GET.get('order_id'))
        form_ins = OrderDelieveryStatusForm(instance=order_obj)
        context = {
            'form':form_ins,
            'order_id':request.GET.get('order_id')
        }
        return render(request, 'orders/order_status_form.html', context)
    
    raise PermissionDenied()

@login_required
def OrderStatus(request,pk):
    if request.method == "POST":
        form = OrderDelieveryStatusForm(request.POST)
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


@login_required
@api_view(['GET'])
def OrderCountGraphApi(request):
    order_obj = Order.objects.all().values(dated=Trunc('ordered_at','month')).annotate(counted=Count('id')).values('dated','counted').order_by('dated')
    serializer_obj = OrderGraphSerializer(order_obj, many=True)
    return Response(serializer_obj.data)