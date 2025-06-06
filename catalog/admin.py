from django.contrib import admin
from .models import Category, Brand, Color, Size, Product, ProductLike

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(ProductLike)
