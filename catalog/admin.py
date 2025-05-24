from django.contrib import admin
from .models import Category, Brand, Color, Size, Product

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Product)
# Register your models here.