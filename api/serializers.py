from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, ProductImage

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'images', 'price']

    def get_images(self, obj):
        images = obj.images.all()
        return ProductImageSerializer(images, many=True).data

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'images', 'price', 'description']

    def get_images(self, obj):
        images = obj.images.all()
        return ProductImageSerializer(images, many=True).data

class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'images', 'price', 'description']

    def get_images(self, obj):
        images = obj.images.all()
        return ProductImageSerializer(images, many=True).data