from django.urls import path
from .views import (
	UserCreateAPIView, 
	ProductListView, 
	ProductDetailView,
	CartListView,
	CartItemUpdateView,
	CartListDeleteView,
	CartItemCreateView,
	OrderCreateView)
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('products/list/', ProductListView.as_view(), name='products-list'),
    path('products/<int:product_id>/detail/', ProductDetailView.as_view(), name='products-detail'),
    path('cart/', CartListView.as_view(), name='items'),
    path('cart/<int:cart_id>/delete/',CartListDeleteView.as_view(), name='cart-delete'),
    path('cart/items/<int:product_id>/add',CartItemCreateView.as_view(), name='cart-item-add'),
    path('cart/items/<int:item_id>/update/',CartItemUpdateView.as_view(), name='items-update'),
    path('cart/checkout/',OrderCreateView.as_view(), name='checkout'),

]