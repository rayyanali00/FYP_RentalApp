from django.conf.urls import url
from django.urls import path
from products import views

app_name = "products"

urlpatterns = [
    path("products/", views.DashboardClient.as_view(), name="products"),
    path("products_list/", views.ProductListFilter.as_view(), name="products_api")
]