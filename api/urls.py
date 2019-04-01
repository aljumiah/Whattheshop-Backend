from django.urls import path
from .views import (UserCreateAPIView, ProductListView, ProductDetailView)
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('products/list/', ProductListView.as_view(), name='products_list'),
    path('products/<int:product_id>/detail/', ProductDetailView.as_view(), name='products_detail')
]