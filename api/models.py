from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import *

class Category(models.Model):
	name = models.CharField(max_length=50)
	# product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.CASCADE, related_name='categories')

	def __str__(self):
		return self.name
		
class Product(models.Model):
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	description = models.TextField()
	category = models.ManyToManyField(Category, related_name='category_products')
	added_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='products')

class ProductImage(models.Model):
	image = models.ImageField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

class Cart(models.Model):
	total = models.DecimalField(max_digits=6, default=0, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	paid = models.BooleanField(default=False)
	order_date = models.DateTimeField(null=True)

class CartItem(models.Model):
	product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='cart_items')
	quantity = models.IntegerField()
	subtotal = models.DecimalField(max_digits=6, null=True, decimal_places=2)
	cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE, related_name='cart_items')
	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	address = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	image = models.ImageField()


@receiver(pre_save, sender = CartItem)
def get_subtotal(instance, *args, **kwargs):
	instance.subtotal = Decimal(instance.product.price * instance.quantity)
	instance.cart.total = instance.cart.total + instance.subtotal
	instance.cart.save()



