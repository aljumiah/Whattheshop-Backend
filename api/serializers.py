from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, ProductImage , Order , CartItem, Profile, Category

from rest_framework_jwt.settings import api_settings

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(read_only=True)
	class Meta:
		model = User
		fields = ['username', 'password', 'token']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		profile = Profile(user=new_user)
		profile.save()
		order = Order(user=new_user)
		order.save()
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		payload = jwt_payload_handler(new_user)
		validated_data['token'] = jwt_encode_handler(payload)
		return validated_data

class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ['image']

class ProductListSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(many=True)

	class Meta:
		model = Product
		fields = ['id','name', 'images', 'price']
		

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProfileUpdateSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Profile
		fields = ['user', 'address', 'image']

class ProfileDetailSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Profile
		fields = '__all__'

class ProductCreateUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = ['name', 'price', 'description']


class CategorySerializer(serializers.ModelSerializer): 
	
	class Meta:
		model = Category
		fields = ['name']
		

class ProductDetailSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(many=True)
	categories = CategorySerializer(many=True)
	class Meta:
		model = Product
		fields = ['name', 'images', 'price', 'description', 'added_by', 'categories']
		

class CartItemListSerializer(serializers.ModelSerializer): 
	product = ProductDetailSerializer()
	class Meta:
		model = CartItem
		fields = ['order', 'subtotal', 'product', 'subtotal', 'quantity']
	

class OrderSerializer(serializers.ModelSerializer): 
	cart_items = CartItemListSerializer(many=True)
	checkout = serializers.HyperlinkedIdentityField(
			view_name = 'checkout',
			lookup_field = 'id',
			lookup_url_kwarg = 'order_id',
		)
	user = UserSerializer()
	class Meta:
		model = Order
		fields = ['id', 'cart_items', 'total', 'paid', 'order_date', 'user','checkout']

class OrderCreateSerializer(serializers.ModelSerializer): 
	user = UserSerializer(read_only=True)
	class Meta:
		model = Order
		fields = ['user']

class CartItemCreateUpdateSerializer(serializers.ModelSerializer): 
	class Meta:
		model = CartItem
		fields = ['product' ,'quantity', 'order']

	