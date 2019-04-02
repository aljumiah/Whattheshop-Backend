from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, ProductImage , Cart , CartItem, Order, Profile
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

	# def get_images(self, obj):
	# 	images = obj.images.all()
	# 	return ProductImageSerializer(images, many=True).data

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'first_name', 'last_name', 'email']


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

	# def get_images(self, obj):
	# 	images = obj.images.all()
	# 	return ProductImageSerializer(images, many=True).data

class ProductDetailSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(many=True)

	class Meta:
		model = Product
		fields = ['name', 'images', 'price', 'description']

	# def get_images(self, obj):
	# 	images = obj.images.all()
	# 	return ProductImageSerializer(images, many=True).data

class CartItemListSerializer(serializers.ModelSerializer): 
	product = ProductDetailSerializer()

	class Meta:
		model = CartItem
		fields = [ 'product','sub_total', 'quantity']


class CartListSerializer(serializers.ModelSerializer): 
	cart_items = CartItemListSerializer(many=True)
	sub_total=serializers.SerializerMethodField()
	quantity=serializers.SerializerMethodField()
	
	class Meta:
		model = Cart
		fields = ['cart_items', 'sub_total', 'quantity']

	# def get_cart(self, obj):
	# 	cart_items = obj.cart_items.all()
	# 	return CartItemListSerializer(cart_items, many=True).data  

class OrderListSerializer(serializers.ModelSerializer): 
	cart = CartItemListSerializer()
	
	class Meta:
		model = Order
		fields = ['cart', 'date', 'quantity']


class OrderCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = []


class CartItemCreateUpdateSerializer(serializers.ModelSerializer): 
	class Meta:
		model = CartItem
		fields = [ 'quantity']

	