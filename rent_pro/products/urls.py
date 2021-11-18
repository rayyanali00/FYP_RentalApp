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
    path('main-redirect/', views.MainRedirect.as_view(), name="main-redirect"),
    path('checkout/', views.OrderView.as_view(), name="checkout"),
    path('checkout-success/', views.checkout_success, name="checkout-success"),
    path('order-success/', views.Order_Success, name="order-success"),
    path('reset_cart/',views.reset_cart, name="reset-cart"),
    path('delete_cart_product/<int:id>/',views.DeleteSingleProduct, name="delete-cart-product"),
    path('order-list-template/', views.OrderListTemplate, name="order-list-template"),
    path('order-list-api/',views.Order_List, name="order-list-api"),
    path('order-detail-view/<int:pk>/',views.OrderDetailView, name="order-detail-view"),
    
    
    #unused
    path('api-overview/', views.api_overview, name="api-overview"),
    path('product-api/',views.Order_List, name="product-api"),
    path('product-detail/<str:pk>/',views.products_api, name="product-detail"),
]