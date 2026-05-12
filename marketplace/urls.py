from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
path('checkout/', views.checkout, name='checkout'),
    # register
    path('accounts/register/', views.register, name='register'),

    # CART
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/decrease/<int:id>/', views.decrease_cart, name='decrease_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
]

