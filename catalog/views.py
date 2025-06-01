from django.shortcuts import render, get_object_or_404
from .models import Brand, Product, Category
from django.core.cache import cache


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


def search_products(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        cache_key = f"search:{query.lower()}"
        results = cache.get(cache_key)

        if results is None:
            print(f"[Redis] Cache MISS — querying DB for: {query}")
            results = list(Product.objects.filter(name__icontains=query))
            cache.set(cache_key, results, timeout=60 * 10)  # 10 минут
        else:
            print(f"[Redis] Cache HIT for query: {query}")

    return render(request, "catalog/search_results.html", {
        "query": query,
        "results": results
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.review_set.all()  # если связь стандартная
    return render(request, "catalog/product_detail.html", {
        "product": product,
        "reviews": reviews,
    })
