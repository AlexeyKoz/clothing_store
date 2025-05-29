from django.shortcuts import render
from catalog.models import Product
from django.core.cache import cache

def home_view(request):
    cache_key = "popular_products"
    popular_products = cache.get(cache_key)

    if popular_products is None:
        print("[Redis] Popular products: Cache MISS — querying DB")
        popular_products = Product.objects.order_by('-price')[:8]
        cache.set(cache_key, popular_products, timeout=60 * 10)
    else:
        print("[Redis] Popular products: Cache HIT")

    return render(request, 'home.html', {
        "popular_products": popular_products,
    })
