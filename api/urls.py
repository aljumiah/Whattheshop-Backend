from django.urls import path
from .views import (UserCreateAPIView, ProductListView, ProfileUpdate, ProfileDetail,)
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
	path('login/', obtain_jwt_token, name='login'),
	path('register/', UserCreateAPIView.as_view(), name='register'),
	path('products/list/', ProductListView.as_view(), name='products_list'),
	path('profile/<int:user_id>/update/', ProfileUpdate.as_view(), name='profile-update'),
	path('profile/<int:user_id>/detail/', ProfileDetail.as_view(), name='profile-detail'),

]