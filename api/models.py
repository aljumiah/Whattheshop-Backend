from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	description = models.TextField()

class ProductImage(models.Model):
	image = models.ImageField()
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='images')

class Cart(models.Model):
	sub_total = models.DecimalField(max_digits=6, decimal_places=2)
	quantity = models.IntegerField()

class CartItem(models.Model):
	product = models.OneToOneField(Product, null=True, on_delete=models.SET_NULL)
	quantity = models.IntegerField()
	sub_total = models.DecimalField(max_digits=6, decimal_places=2)
	cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL, related_name='cart_items')

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,)
	address = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	image = models.ImageField()

class Order(models.Model):
	cart = models.OneToOneField(Cart, null=True, on_delete=models.SET_NULL)
	quantity = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)
	profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='orders')

