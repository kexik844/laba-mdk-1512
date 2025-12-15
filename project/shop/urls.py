from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<slug:slug>/', views.category_products, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='orders'),
]   