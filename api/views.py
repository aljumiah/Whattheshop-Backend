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
	UserSerializer,
	UserUpdateSerializer,
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
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.template.loader import get_template, render_to_string
from django.template import Context

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer


class ProfileUpdate(APIView):
	permission_classes = [IsAuthenticated, ]

	def put(self, request, *args, **kwargs):
		""" expected request = {user: {<USER_DATA>}, profile{<PROFILE_DATA>}}
			check serializer for more detail on USER_DATA and PROFILE_DATA
		"""
		new_profile = request.data.get('profile')
		new_user = request.data.get('user')
		old_profile = Profile.objects.get(user=self.request.user)

		profileSerializer = ProfileUpdateSerializer(instance= old_profile, data=new_profile, partial=True)
		if profileSerializer.is_valid(raise_exception=True):
			profileSerializer.save()

		userSerializer = UserUpdateSerializer(instance=old_profile.user, data=new_user, partial=True)
		if userSerializer.is_valid(raise_exception=True):
			userSerializer.save()
		
		return Response({"success": "Profile for '{}' updated successfully".format(old_profile.user.username)})


class ProfileDetail(APIView):
	permission_classes = [IsAuthenticated, ]

	def get(self, request):
		profile = Profile.objects.get(user=self.request.user)
		serializer = ProfileDetailSerializer(profile)
		return Response(serializer.data)


class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer


class CartItemCreateView(APIView):
	serializer_class = CartItemCreateUpdateSerializer
	permission_classes = [IsAuthenticated, ]

	def post(self, request, order_id, product_id):	
		product = Product.objects.get(id=product_id)
		order = Order.objects.get(id=order_id)
		serializer = CartItemCreateUpdateSerializer(data=request.data, partial=True)
		cart_item, created = CartItem.objects.get_or_create(product=product, order=order)
		if serializer.is_valid(raise_exception=True):
			valid_data = serializer.data
			if created:
				cart_item.quantity = valid_data['quantity']
				cart_item.product.stock -= cart_item.quantity
				cart_item.save()
				cart_item.product.save()
			else:
				cart_item.quantity += valid_data['quantity']
				cart_item.product.stock -= valid_data['quantity']
				cart_item.save()
				cart_item.product.save()
			return Response({"quantity":valid_data['quantity']},status=status.HTTP_200_OK)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CartItemUpdateView(RetrieveUpdateAPIView):
	# queryset = CartItem.objects.all()
	serializer_class = CartItemCreateUpdateSerializer
	# lookup_field = 'id'
	# lookup_url_kwarg = 'item_id'
	permission_classes = [IsAuthenticated, ]
	
	def put(self, request, item_id):
		my_data = request.data
		cartItem = CartItem.objects.get(id=item_id)
		product = Product.objects.get(id=cartItem.product.id)
		order = Order.objects.get(id=cartItem.order.id)
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			vaild_data = serializer.data
			# old_total= (cartItem.quantity * cartItem.product.price)
			# new_total = (vaild_data['quantity']* product.price)
			# order.total = order.total - old_total +new_total
			# cartItem.subtotal=new_total
			# order.save()
			old_stock= product.stock + cartItem.quantity
			new_stock = old_stock - vaild_data['quantity']
			product.stock =new_stock
			cartItem.quantity=vaild_data['quantity']
			cartItem.save()
			product.save()
			return Response(CartItemCreateUpdateSerializer(cartItem).data,status=status.HTTP_200_OK)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)		


class CartItemDeleteView(DestroyAPIView):
	queryset = CartItem.objects.all()
	serializer_class = CartItemListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'item_id'
	permission_classes = [IsAuthenticated, ]


class CategoriesListView(ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class OrderView(APIView):
	permission_classes = [IsAuthenticated, ]

	def get(self, request):
		order, resp = Order.objects.get_or_create(user=self.request.user, paid=False)
		serializer = OrderSerializer(order)
		return Response(serializer.data)


class OrderPaymentView(APIView):
	def post(self, request, order_id):
		order = Order.objects.get(id=order_id)
		print(request.data)
		phonenumber = request.data['phoneNumber']
		url = "https://api.tap.company/v2/charges"
		total = str(order.get_total())
		if(request.data['requestFrom'] == "js"):
			payload = "{\"amount\":" + total + ",\"currency\":\"SAR\",\"threeDSecure\":true,\"customer\":{\"first_name\":\""+order.user.first_name+"\",\"last_name\":\""+order.user.last_name+"\",\"email\":\""+order.user.email+"\",\"phone\":{\"country_code\":\"966\",\"number\":\""+phonenumber+"\"}},\"source\":{\"id\":\"src_all\"},\"redirect\":{\"url\":\"http://localhost:3000/thank-you/\"}}"
		elif(request.data['requestFrom'] == "native"):
			payload = "{\"amount\":" + total + ",\"currency\":\"SAR\",\"threeDSecure\":true,\"customer\":{\"first_name\":\""+order.user.first_name+"\",\"last_name\":\""+order.user.last_name+"\",\"email\":\""+order.user.email+"\",\"phone\":{\"country_code\":\"966\",\"number\":\""+phonenumber+"\"}},\"source\":{\"id\":\"src_all\"},\"redirect\":{\"url\":\"exp://172.20.10.3:19000/\"}}"
		headers = {
			'authorization': "Bearer sk_test_XKokBfNWv6FIYuTMg5sLPjhJ",
			'content-type': "application/json"
			}
		print("its here")

		response = requests.request("POST", url, data=payload, headers=headers)
		print(response.json())
		return Response({"response":response, "order": OrderSerializer(order).data})

class OrderCheckoutView(APIView):
	permission_classes = [IsAuthenticated, ]
	
	def post(self,request, order_id):
		order = Order.objects.get(id=order_id)
		
		serializer = OrderSerializer(instance = order, data={"paid": True, "order_date":datetime.datetime.now()}, partial=True)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			"""		EMAIL SETUP 		"""
			subject = "Your Checkout Has Been Completed!"
			order_summary = ""
			plain_msg = """total : %s """ % (str(serializer.data['total']))
			html_msg = get_template('checkout_email.html').render({ 'order': order, 'total': serializer.data['total'] })

			if self.request.user.email:
				send_mail(subject, plain_msg, settings.EMAIL_HOST_USER, [self.request.user.email,], fail_silently=False, html_message=html_msg)

			return Response(serializer.data)


class OrderHistoryView(ListAPIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated, ]
	def get_queryset (self):
		queryset = Order.objects.filter(user=self.request.user, paid=True)
		return queryset


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


