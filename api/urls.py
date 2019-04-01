from django.urls import path
from .views import (
UserCreateAPIView,
 ProductListView, 
 ProductImageAddView,
 ProductDetailView,
 ProductUpdateView, 
 ProductDeleteView, 
 ProductCreateView,
 ProductImageDeleteView,
 ProductImageUpdateView,
 CartListView,
 CartItemUpdateView,
 CartListDeleteView,
 CartItemCreateView,
 OrderCreateView,
 ProfileUpdate,
 ProfileDetail,
  )
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('products/list/', ProductListView.as_view(), name='products-list'),

    path('products/<int:product_id>/detail/', ProductDetailView.as_view(), name='products-detail'),
    path('products/<int:product_id>/update/', ProductUpdateView.as_view(), name='products-update'),
    path('products/<int:product_id>/delete/', ProductDeleteView.as_view(), name='products-delete'),
    path('products/create/', ProductCreateView.as_view(), name='products-update'),
    path('products/<int:product_id>/image/add/', ProductImageAddView.as_view(), name='product-image-add'),
    path('products/<int:product_id>/image/<int:image_id>/update/', ProductImageUpdateView.as_view(), name='product-image-update'),
    path('products/<int:product_id>/image/<int:image_id>/delete/', ProductImageDeleteView.as_view(), name='product-image-delete'),
    
    path('cart/', CartListView.as_view(), name='items'),
    path('cart/<int:cart_id>/delete/',CartListDeleteView.as_view(), name='cart-delete'),
    path('cart/items/<int:product_id>/add',CartItemCreateView.as_view(), name='cart-item-add'),
    path('cart/items/<int:item_id>/update/',CartItemUpdateView.as_view(), name='items-update'),
    path('cart/checkout/',OrderCreateView.as_view(), name='checkout'),
  
    path('profile/<int:user_id>/update/', ProfileUpdate.as_view(), name='profile-update'),
    path('profile/<int:user_id>/detail/', ProfileDetail.as_view(), name='profile-detail'),
]