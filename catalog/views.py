from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .models import Brand

def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'catalog/brands_list.html', {'brands': brands})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'catalog/category.html', {
        'category': category,
        'products': products

    })

def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'catalog/brands_list.html', {'brands': brands})