"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('shop/ <str:cat>/', views.shop, name='shop'),
    path('home_2/', views.home_2, name='home_2'),
    path('home_3/', views.home_3, name='home_3'),
    path('shoping_cart/', views.shoping_cart, name='shoping_cart'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout, name='logout'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('forgetpassword_phone/', views.forgetpassword_phone, name='forgetpassword_phone'),
    path('otp/', views.otp, name='otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/', views.profile, name='profile'),
    path('add_product/', views.add_product, name='add_product'),
    path('view_product/', views.view_product, name='view_product'),
    path('product_details/ <int:pk>/', views.product_details, name='product_details'),
    path('seller_index/', views.seller_index, name='seller_index'),
    path('product_edit/ <int:pk>/', views.product_edit, name='product_edit'),
    path('product_delete/ <int:pk>/', views.product_delete, name='product_delete'),
    path('buyer_product_details/ <int:pk>/', views.buyer_product_details, name='buyer_product_details'),
    path('add_to_wishlist/ <int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('delete_wishlist/ <int:pk>/', views.delete_wishlist, name='delete_wishlist'),
    path('add_to_cart/ <int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart/ <int:pk>/', views.delete_cart, name='delete_cart'),
    path('change_quantity/ <int:pk>/', views.change_quantity, name='change_quantity'),
    path('order_details', views.order_details, name='order_details'),
    path('check_out/', views.check_out, name='check_out'),
    path('success/', views.success, name='success'),
    # path('order/', views.order, name='order'),
    # path('delete_address/', views.delete_address, name='delete_address'),
    
    
]
