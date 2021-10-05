from django.conf.urls import url
from django.urls import path
from products import views

app_name = "products"

urlpatterns = [
    path("products/", views.DashboardClient.as_view(), name="products"),
    path("products_list/", views.ProductListFilter.as_view(), name="products_api"),
    path("product_detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product_cat/", views.ProductCategoryApi, name="product_api")
]