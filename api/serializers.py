from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, ProductImage , Order , CartItem, Profile, Category
from rest_framework_jwt.settings import api_settings

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'token']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(new_user)
        token = jwt_encode_handler(payload)

        validated_data["token"] = token
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError(
                "Incorrect username/password combination! Noob..")

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)

        data["token"] = token
        return data

class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ['image']


class CategorySerializer(serializers.ModelSerializer): 
	
	class Meta:
		model = Category
		fields = ['name']


class ProductListSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(many=True)
	categories = CategorySerializer(many=True)
	class Meta:
		model = Product
		fields = '__all__'


class CartItemListSerializer(serializers.ModelSerializer): 
	product = ProductListSerializer()
	#order=OrderSerializer()
	class Meta:
		model = CartItem
		fields = ['id','order', 'product', 'subtotal', 'quantity']
	

class OrderHistorySerializer(serializers.ModelSerializer): 
	cart_items = CartItemListSerializer(many=True)
	total = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = ['id', 'cart_items', 'total', 'paid', 'order_date']

	def get_total(self, obj):
		return obj.get_total()

class UserSerializer(serializers.ModelSerializer):
	orders = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name', 'email', 'orders']

	def get_orders(self, obj):
		return OrderHistorySerializer(obj.orders.all(), many=True).data

#changes
class UserUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['address']


class ProfileDetailSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Profile
		fields = '__all__'

class ProductCreateUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = ['name', 'price', 'description', 'stock']


class OrderSerializer(serializers.ModelSerializer): 
	cart_items = CartItemListSerializer(many=True)
	checkout = serializers.HyperlinkedIdentityField(
			view_name = 'checkout',
			lookup_field = 'id',
			lookup_url_kwarg = 'order_id',
		)
	user = UserSerializer()
	total = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = ['id', 'cart_items', 'total', 'paid', 'order_date', 'user','checkout']

	def get_total(self, obj):
		print(obj.get_total())
		return obj.get_total()

class OrderCreateSerializer(serializers.ModelSerializer): 
	user = UserSerializer(read_only=True)
	class Meta:
		model = Order
		fields = ['user']

class CartItemCreateUpdateSerializer(serializers.ModelSerializer): 
	class Meta:
		model = CartItem
		fields = ['id','product' ,'quantity', 'order']

	