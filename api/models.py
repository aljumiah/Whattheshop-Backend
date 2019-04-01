from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	name= models.CharField(max_length=50)
	price= models.DecimalField(max_digits=6, decimal_places=2)
	description = models.TextField()

class ProductImages(models.Model):
	image = models.ImageField()
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='images')

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,)
	address = models.TextField()
	# order_history = models.DateTimeField(auto_now_add=True)
	created_on = models.DateTimeField(auto_now_add=True)
	image = models.ImageField()