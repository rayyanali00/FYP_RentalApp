from django.core.mail import message
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse,reverse_lazy
import stripe
from django.conf import settings;
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from .serializers import PaymentSerializer
from django.contrib.auth.decorators import login_required
from products.models import Order
from users.models import User
from django.core.mail import send_mail,EmailMultiAlternatives


stripe.api_key = settings.STRIPE_PRIVATE_KEY

# Create your views here.
def payment_form(request):
    print("*****************")
    print(request.GET.get('order_id'))
    context = {}
    order_obj = Order.objects.get(order_id=request.GET.get('order_id'))
    context['email'] = order_obj.email
    context['your_bid_total'] = order_obj.your_bid_total
    context['name']=order_obj.email.split('@')[0]
    context['order_id'] = request.GET.get('order_id')
    return render(request, 'payment_form.html', context=context)

def payment_success(request):
    return render(request, 'payment_success.html')

def charge_user(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        customer = stripe.Customer.create(
            email = request.POST['email'],
            name = request.POST['name'],
            source = request.POST['stripeToken']
        )
        try:
            charge = stripe.Charge.create(
    customer = customer,
    amount = amount*100,
    currency = 'usd',
    description = 'Rent Payment'
    )
            subject, from_email, to = 'Order Accepted', settings.EMAIL_HOST_USER, request.POST['email']
            text_content = ''
            html_content = f'<h1>Payment Succeed</h1> <h2>Your payment has been recieved, you will recieve your items on your requested delievery date<h2> <h3>Order Id : {request.POST.get("order_id")}</h3>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print(request.POST.get('order_id'))
            order_obj = Order.objects.filter(order_id=request.POST.get('order_id')).update(payment_process="Received")
        except stripe.error.CardError as e:
            messages.warning(request, e.user_message)
    return redirect(reverse('payments:payment-success'))

@login_required
@api_view(['GET'])
def ProcessPaymentDataApi(request):
    print(request.user.user_role)
    if request.user.user_role == "General":
        user_obj = User.objects.get(email=request.user.email)
        pay_obj = Order.objects.filter(user=user_obj,is_accepted="Accept",payment_process='pending')
    else:
        print("elseeeeeeeeee")
        pay_obj = Order.objects.filter(is_accepted="Accept",payment_process='pending')
    serializer_obj = PaymentSerializer(pay_obj, many=True)
    return Response(serializer_obj.data)

@login_required
def payment_list_template(request):
    return render(request, 'process-payment-list.html')
