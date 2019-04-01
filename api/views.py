from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, )
from .serializers import (UserCreateSerializer, ProductListSerializer, )
from .models import Product

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer
