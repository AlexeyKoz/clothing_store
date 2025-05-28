from django.shortcuts import render, get_object_or_404
from .models import Brand, Product, Category

def brand_list(request):
    brands = Brand.objects.all()
    return render(request, "catalog/brand_list.html", {"brands": brands})

def products_by_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    products = Product.objects.filter(brand=brand)
    return render(request, "catalog/products_by_brand.html", {
        "brand": brand,
        "products": products
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, "catalog/products_by_category.html", {
        "category": category,
        "products": products
    })

