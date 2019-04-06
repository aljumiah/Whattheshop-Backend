from django.urls import path
from .views import (
UserCreateAPIView,
 ProductListView, 
 ProductImageAddView,
 ProductUpdateView, 
 ProductDeleteView, 
 ProductCreateView,
 ProductImageDeleteView,
 ProductImageUpdateView,
 CartItemUpdateView,
 CartItemCreateView,
 ProfileUpdate,
 ProfileDetail,
 OrderCheckoutView,
 OrderHistoryView,
 CartItemDeleteView,
 CartListView,
 CategoriesListView,
 UserLoginAPIView,
 UserCreateAPIView,
  )
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
	#path('login/', obtain_jwt_token, name='login'),
	#path('register/', UserCreateAPIView.as_view(), name='register'),
	
	path('login/', UserLoginAPIView.as_view(), name='login'),
	path('signup/', UserCreateAPIView.as_view(), name='register'),

	path('profile/', ProfileDetail.as_view(), name='profile-detail'),
	path('profile/update/', ProfileUpdate.as_view(), name='profile-update'),
	
	path('categories/list/', CategoriesListView.as_view(), name='categories'),
	path('products/list/', ProductListView.as_view(), name='products-list'),

	path('products/create/', ProductCreateView.as_view(), name='products-update'),
	path('products/<int:product_id>/update/', ProductUpdateView.as_view(), name='products-update'),
	path('products/<int:product_id>/delete/', ProductDeleteView.as_view(), name='products-delete'),
	
	path('products/<int:product_id>/image/add/', ProductImageAddView.as_view(), name='product-image-add'),
	path('products/<int:product_id>/image/<int:image_id>/update/', ProductImageUpdateView.as_view(), name='product-image-update'),
	path('products/<int:product_id>/image/<int:image_id>/delete/', ProductImageDeleteView.as_view(), name='product-image-delete'),
	

	path('order/<int:order_id>/items/<int:product_id>/add/', CartItemCreateView.as_view(), name='item-add'),
	
	path('order/items/', CartListView.as_view(), name='cart'),
	
	path('items/<int:item_id>/update/', CartItemUpdateView.as_view(), name='items-update'),
	path('items/<int:item_id>/delete/', CartItemDeleteView.as_view(), name='items-delete'),

	path('order/<int:order_id>/checkout/', OrderCheckoutView.as_view(), name='checkout'),
	
	
]