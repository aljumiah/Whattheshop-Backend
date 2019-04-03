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
	CartItemCreateUpdateSerializer,
	OrderSerializer,
	ProductCreateUpdateSerializer,
	ProductImageSerializer,
	ProfileUpdateSerializer,
	ProfileDetailSerializer,
	OrderCreateSerializer,
	CategorySerializer,
)
from .models import Product, CartItem, Order, Profile, ProductImage
from django.contrib.auth.models import User
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, )
import datetime
class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer

class ProfileUpdate(RetrieveUpdateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileUpdateSerializer
	lookup_field='id'
	lookup_url_kwarg = 'user_id'
	permission_classes = [IsAuthenticated, ]

class ProfileDetail(RetrieveAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'user_id'
	permission_classes = [IsAuthenticated, ]

class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer

class ProductDetailView(RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'

class CartItemCreateView(CreateAPIView):
	serializer_class = CartItemCreateUpdateSerializer
	permission_classes = [IsAuthenticated, ]

	def perform_create(self, serializer):	
		product = Product.objects.get(id=self.kwargs['product_id'])
		order = Order.objects.get(id=self.kwargs['order_id'])
		serializer.save(product=product, order=order)

class CartItemUpdateView(RetrieveUpdateAPIView):
	queryset = CartItem.objects.all()
	serializer_class = CartItemCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'item_id'
	permission_classes = [IsAuthenticated, ]

#Cart 
class CartListView(ListAPIView):
	serializer_class = CartItemListSerializer
	permission_classes = [IsAuthenticated, ]
	def get_queryset(self):
		queryset = CartItem.objects.filter(order__user=self.request.user)
		return queryset


class OrderCheckoutView(CreateAPIView):
	serializer_class = OrderCreateSerializer
	permission_classes = [IsAuthenticated, ]
	
	def perform_create(self,serializer):
		order = Order.objects.get(id=self.kwargs['order_id'])
		order.paid= True
		order.order_date = datetime.datetime.now()
		order.save()
		serializer.save(user=self.request.user)

class OrderHistoryView(ListAPIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated, ]
	def get_queryset (self):
		queryset = Order.objects.filter(user=self.request.user, paid=True)
		return queryset

class CartItemDeleteView(DestroyAPIView):
	queryset = CartItem.objects.all()
	serializer_class = CartItemListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'item_id'
	permission_classes = [IsAuthenticated, ]

class ProductUpdateView(RetrieveUpdateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'	
	permission_classes = [IsAuthenticated, ]

class ProductCreateView(CreateAPIView):
	serializer_class = ProductCreateUpdateSerializer
	permission_classes = [IsAuthenticated, ]
	def perform_create(self, serializer):
		serializer.save(added_by=self.request.user)

class ProductDeleteView(DestroyAPIView):
	queryset = Product.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'	
	permission_classes = [IsAdminUser, ]

class ProductImageAddView(CreateAPIView):
	serializer_class = ProductImageSerializer
	permission_classes = [IsAuthenticated, ]

	def perform_create(self, serializer):
		product = Product.objects.get(id=self.kwargs['product_id'])
		serializer.save(product=product)

class ProductImageUpdateView(RetrieveUpdateAPIView):
	serializer_class = ProductImageSerializer
	permission_classes = [IsAuthenticated, ]
	lookup_field = 'id'
	lookup_url_kwarg = 'image_id'
	def get_queryset(self):
		images = ProductImage.objects.filter(product__id=self.kwargs['product_id'])
		return images
	
class ProductImageDeleteView(DestroyAPIView):
	permission_classes = [IsAuthenticated, ]
	lookup_field = 'id'
	lookup_url_kwarg = 'image_id'
	def get_queryset(self):
		images = ProductImage.objects.filter(product__id=self.kwargs['product_id'])
		return images
