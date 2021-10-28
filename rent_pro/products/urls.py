from django.conf.urls import url
from django.urls import path
from products import views
from products.utils import get_cart_data

app_name = "products"

urlpatterns = [
    path("products/", views.DashboardClient.as_view(), name="products"),
    path("products_list/", views.ProductListFilter.as_view(), name="products_api"),
    path("product_detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product_cat/", views.ProductCategoryApi, name="product_api"),
    path('get_book_products/',views.get_cart_data, name="book-products"),
    path('cart/', views.CartSystem, name='get-cart-api'),
    path('main-redirect/', views.MainRedirect.as_view(), name="main-redirect")
]