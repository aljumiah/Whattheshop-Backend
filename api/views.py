from rest_framework.generics import (
	CreateAPIView, 
	ListAPIView, 
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView )
from .serializers import (
	UserCreateSerializer, 
	ProductListSerializer, 
	ProductDetailSerializer,
	CartItemListSerializer,
	CartListSerializer,
	CartItemCreateUpdateSerializer,
	OrderCreateSerializer )
from .models import Product, CartItem, Cart, Profile

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer

class ProductDetailView(RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'

class CartListView(ListAPIView):
	queryset = Cart.objects.all()
	serializer_class = CartListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'item_id'

class CartItemUpdateView(RetrieveUpdateAPIView):
	queryset = CartItem.objects.all()
	serializer_class = CartItemCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'item_id'

class CartItemCreateView(CreateAPIView):
	serializer_class = CartItemCreateUpdateSerializer

	def perform_create(self, serializer):	
		product= Product.objects.get(id=self.kwargs['product_id'])
		serializer.save(product=product)

class CartListDeleteView(DestroyAPIView):
	queryset = Cart.objects.all()
	serializer_class = CartListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'cart_id'

class OrderCreateView(CreateAPIView):
	serializer_class=OrderCreateSerializer

	def perform_create(self, serializer):	
		cart = Cart.objects.get(user=self.request.user)
		profile = Profile.objects.get(user=self.request.user)
		serializer.save(cart=cart, profile=profile)
