from django.contrib import admin
from .models import Product, ProductImages, Cart

admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Cart)