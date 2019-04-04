from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from decimal import Decimal

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name	
  
class Product(models.Model):
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField()
	categories = models.ManyToManyField(Category, related_name='category_products')
	added_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='products')
	stock =models.IntegerField()
	
	def __str__(self):
		return self.name

class ProductImage(models.Model):
	image = models.ImageField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

class Order(models.Model):
	total = models.DecimalField(max_digits=10, default=0, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	paid = models.BooleanField(default=False) 
	order_date = models.DateTimeField(null=True)

class CartItem(models.Model):
	product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='cart_items')
	quantity = models.IntegerField()
	subtotal = models.DecimalField(default=0.00,max_digits=10, null=True, decimal_places=2)
	order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='cart_items')
	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	address = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	image = models.ImageField()


@receiver(pre_save, sender = CartItem)
def get_subtotal(instance, *args, **kwargs):
    instance.subtotal = Decimal(instance.product.price)*Decimal(instance.quantity)
    instance.order.total = Decimal(instance.order.total) + instance.subtotal
    instance.product.stock = int(instance.product.stock) - int(instance.quantity)
    instance.product.save()
    instance.order.save()

@receiver(pre_delete, sender = CartItem)
def change_subtotal(instance, *args, **kwargs):
    instance.order.total = Decimal(instance.order.total) - instance.subtotal
    instance.product.stock = int(instance.product.stock) + int(instance.quantity)
    instance.product.save()
    instance.order.save()

