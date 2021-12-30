from django.conf.urls import url
from django.urls import path
from payments import views

app_name = "payments"

urlpatterns = [
    path('payment-form/', views.payment_form, name="payment-form"),
    path('payment-success/', views.payment_success, name="payment-success"),
    path('payment-process-api/', views.ProcessPaymentDataApi, name="process-payment-api"),
    path('payment-process-template/', views.payment_list_template, name="payment-list-templates"),
    path('charge-user/', views.charge_user, name="charge-user"),
]