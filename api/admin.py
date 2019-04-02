from django.contrib import admin
from .models import Product, ProductImage, CartItem, Cart, Profile

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(CartItem)
admin.site.register(Cart)
