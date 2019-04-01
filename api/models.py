from django.db import models

class Product(models.Model):
	name= models.CharField(max_length=50)
	price= models.DecimalField(max_digits=6, decimal_places=2)
	description = models.TextField()

class ProductImages(models.Model):
	image = models.ImageField()
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='images')

class Cart(models.Model):
	#Edit the model name
	cart_Item = models.OneToOneField(Product, null=True, on_delete=models.SET_NULL, related_name='items')
	sub_total= models.DecimalField(max_digits=6, decimal_places=2)
	quentity= models.IntegerField()