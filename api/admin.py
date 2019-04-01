from django.contrib import admin
from .models import Product, ProductImages, Profile

admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Profile)