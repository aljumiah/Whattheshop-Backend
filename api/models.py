from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import *
class Product(models.Model):
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	description = models.TextField()
	added_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='products')

class ProductImage(models.Model):
	image = models.ImageField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

class Cart(models.Model):
	total = models.DecimalField(max_digits=6, decimal_places=2)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	paid = models.BooleanField(default=False) 
	order_date = models.DateTimeField(null=True)

class CartItem(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	subtotal = models.DecimalField(max_digits=6, null=True, decimal_places=2)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	address = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	image = models.ImageField()

@receiver(pre_save, sender = CartItem)
def get_subtotal(instance, *args, **kwargs):
	instance.subtotal = Decimal(instance.product.price * instance.quantity)

@receiver(post_save, sender = Cart)
def get_total(instance,*args, **kwargs):
	print("test")
	instance.total = sum(instance.cart_items.values_list('subtotal')[0])