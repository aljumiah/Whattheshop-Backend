from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView)
from .serializers import (UserCreateSerializer, ProductListSerializer, ProfileUpdateSerializer, ProfileDetailSerializer )
from .models import Product, Profile

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer

class ProfileUpdate(RetrieveUpdateAPIView):
	serializer_class = ProfileUpdateSerializer
	lookup_field='id'
	lookup_url_kwarg = 'user_id'
	def get_queryset(self):
		queryset = Profile.objects.filter(user__id = self.kwargs['user_id'])
		return queryset

class ProfileDetail(RetrieveAPIView):
	queryset = ProfileUpdateSerializer
	serializer_class = ProfileDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'user_id'
	def get_queryset(self):
		queryset = Profile.objects.filter(user__id = self.kwargs['user_id'])
		return queryset
    

