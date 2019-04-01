from django.db import models

class Product(models.Model):
	name= models.CharField(max_length=50)
	price= models.DecimalField(max_digits=6, decimal_places=2)
	description = models.TextField()

class ProductImages(models.Model):
	image = models.ImageField()
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='images')

class CartItem(models.Model):
	product = models.OneToOneField(Product, null=True, on_delete=models.SET_NULL, related_name='items')
	quantity = models.IntegerField()
	sub_total= models.DecimalField(max_digits=6, decimal_places=2)

class Order(models.Model):
	car_Item = models.OneToOneField(CartItem, null=True, on_delete=models.SET_NULL, related_name='items')
	quantity = models.IntegerField()
	date= models.DateField()
	

