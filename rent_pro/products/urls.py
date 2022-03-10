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
    path('order-detail-template/<int:pk>/<str:order_id>', views.OrderDetailTemplate, name="order-detail-template"),
    path('order-detail-api/<int:pk>/<str:order_id>',views.OrderDetailApi, name="order-detail-api"),
    path('order-status/',views.OrderStatusUpdate, name="order-status"),
    path('order-status-form/<str:pk>/',views.OrderStatus, name="order-status-form"),
    path('product-api/',views.products_api, name="product-api"),
    path('product-list-template/',views.product_list_template, name="product-list-template"),
    path('create-product/',views.CreateProduct.as_view(), name="create-product"),
    path('delete-product/<int:pk>',views.ProductDelete, name="delete-product"),
    path('update-product/<int:pk>',views.UpdateProduct.as_view(), name="update-product"),
    # path('test/<str:id>/',views.test_view, name="test-view"),
    
    path('order-request-template/',views.OrderRequestTemplate, name="order-request-template"),
    path('order-request-api/',views.Order_Request, name="order-request-api"),
    
    path('pending-orders-list/',views.PendingOrderListTemplate, name="pending-order-template"),
    path('pending-orders-api/',views.PendingOrderApi, name="pending-order-api"),
    
    path('delievered-orders-list/',views.DelieveredOrderListTemplate, name="delievered-orders-template"),
    path('delievered-orders-api/',views.DelieveredOrderApi, name="delievred-orders-api"),
    
    path('order-request-form/',views.OrderRequestForm, name="order-request-form"),
    path('order-request-status/',views.OrderRequestStatus, name="order-request-status"),
    
    path('send-return-email/',views.SendReturnEmailList, name="send-return-email"),
    path('items-list/',views.ItemListApi, name='item-list-api'),
    path('send-email-form/',views.SendEmailForm, name='send-email-form'),
    path('send-email/', views.SendReturnEmail, name='send-email'),
    
    path('OrderCountGraphApi/',views.OrderCountGraphApi, name="order-graph-api"),
    
    #unused
    # path('api-overview/', views.api_overview, name="api-overview"),
    path('product-api/',views.Order_List, name="product-api"),
    path('product-detail/<str:pk>/',views.products_api, name="product-detail"),
]