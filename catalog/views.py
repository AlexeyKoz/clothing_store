from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Brand, Product, Category, ProductLike
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from reviews.models import Review
from django.db import models


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
    products = (
        Product.objects.filter(category=category)
        .annotate(num_likes=models.Count('likes'))
        .order_by('-num_likes', '-price')
    )
    # Prepare product info with like status and count
    product_infos = []
    user = request.user if request.user.is_authenticated else None
    for product in products:
        liked = False
        if user:
            liked = product.likes.filter(user=user).exists()
        like_count = product.likes.count()
        product_infos.append({
            'product': product,
            'liked': liked,
            'like_count': like_count,
        })
    return render(request, "catalog/products_by_category.html", {
        "category": category,
        "product_infos": product_infos,
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


# Добавьте этот импорт в начало файла catalog/views.py:


# Замените существующую функцию product_detail на эту:
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')
    liked = False
    user_has_review = False

    if request.user.is_authenticated:
        liked = ProductLike.objects.filter(
            user=request.user, product=product
        ).exists()
        user_has_review = Review.objects.filter(
            user=request.user, product=product
        ).exists()

    like_count = product.likes.count()

    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "liked": liked,
            "like_count": like_count,
            "user_has_review": user_has_review,
        },
    )


@require_POST
@login_required
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    like, created = ProductLike.objects.get_or_create(
        user=request.user, product=product)
    if not created:
        like.delete()
        messages.info(request, "Like Deleted.")
    else:
        messages.success(request, "I like it !")
    return HttpResponseRedirect(
        request.META.get("HTTP_REFERER", reverse(
            "catalog:product_detail", args=[product_id]))
    )
