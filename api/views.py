from rest_framework.generics import (
	CreateAPIView, 
	ListAPIView, 
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
)
from rest_framework.views import APIView
from .serializers import (
	UserCreateSerializer, 
	ProductListSerializer, 
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
from .models import Product, CartItem, Order, Profile, ProductImage, Category
from django.contrib.auth.models import User
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, )
import datetime
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer


class ProfileUpdate(APIView):
	# queryset = Profile.objects.all()
	# serializer_class = ProfileUpdateSerializer
	# lookup_field='id'
	# lookup_url_kwarg = 'user_id'
	permission_classes = [IsAuthenticated, ]

	# def put(self, request, user_id, *args, **kwargs):
	# 	pass

class ProfileDetail(APIView):
	# serializer_class = ProfileDetailSerializer
	permission_classes = [IsAuthenticated, ]

	def get(self, request):
		profile = Profile.objects.get(user=self.request.user)
		serializer = ProfileDetailSerializer(profile)
		return Response(serializer.data)


class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer


class CartItemCreateView(CreateAPIView):
	serializer_class = CartItemCreateUpdateSerializer
	permission_classes = [IsAuthenticated, ]

	def perform_create(self, serializer):	
		product = Product.objects.get(id=self.kwargs['product_id'])
		order = Order.objects.get(id=self.kwargs['order_id'])
		serializer.save(product=product, order=order)


class CartItemUpdateView(RetrieveUpdateAPIView):
    # queryset = CartItem.objects.all()
    serializer_class = CartItemCreateUpdateSerializer
    # lookup_field = ‘id’
    # lookup_url_kwarg = ‘item_id’
    permission_classes = [IsAuthenticated, ]
    
    def put(self, request, item_id):
        my_data = request.data
        cartItem = CartItem.objects.get(id=item_id)
        product = Product.objects.get(id=cartItem.product.id)
        order = Order.objects.get(id=cartItem.order.id)
        serializer = self.serializer_class(data=my_data)
        if serializer.is_valid():
            vaild_data = serializer.data
            old_total= (cartItem.quantity * cartItem.product.price)
            new_total = (vaild_data['quantity']* product.price)
            order.total = order.total - old_total +new_total
            cartItem.subtotal=new_total
            order.save()
            old_stock= product.stock + cartItem.quantity
            print(old_stock)
            new_stock = old_stock - vaild_data['quantity']
            print(new_stock)
            product.stock =new_stock
            cartItem.quantity=vaild_data['quantity']
            cartItem.save()
            product.save()
            return Response(CartItemCreateUpdateSerializer(cartItem).data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


class CategoriesListView(ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

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
