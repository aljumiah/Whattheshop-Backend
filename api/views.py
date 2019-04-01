from rest_framework.generics import (
	CreateAPIView, 
	ListAPIView, 
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
)
from .serializers import (
	UserCreateSerializer, 
	ProductListSerializer, 
	ProductDetailSerializer,
	CartItemListSerializer,
	CartListSerializer,
	CartItemCreateUpdateSerializer,
	OrderCreateSerializer,
  ProductCreateUpdateSerializer,
  ProductImageSerializer,
  ProfileUpdateSerializer,
  ProfileDetailSerializer,
)
from .models import Product, CartItem, Cart, Profile, ProductImage

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

class ProductUpdateView(RetrieveUpdateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'	

class ProductCreateView(CreateAPIView):
	serializer_class = ProductCreateUpdateSerializer

class ProductDeleteView(DestroyAPIView):
	queryset = Product.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'	

class ProductImageAddView(CreateAPIView):
	serializer_class = ProductImageSerializer
	
	def perform_create(self, serializer):
		product = Product.objects.get(id=self.kwargs['product_id'])
		serializer.save(product=product)

class ProductImageUpdateView(RetrieveUpdateAPIView):
	serializer_class = ProductImageSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'image_id'
	def get_queryset(self):
		images = ProductImage.objects.filter(product__id=self.kwargs['product_id'])
		return images
	
class ProductImageDeleteView(DestroyAPIView):
	lookup_field = 'id'
	lookup_url_kwarg = 'image_id'
	def get_queryset(self):
		images = ProductImage.objects.filter(product__id=self.kwargs['product_id'])
		return images
