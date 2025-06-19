from django.shortcuts import render
from catalog.models import Product, ProductLike
from django.core.cache import cache
from django.db import models


def home_view(request):
    # Order products by number of likes (popularity), then by price
    popular_products = (
        Product.objects.annotate(num_likes=models.Count('likes'))
        .order_by('-num_likes', '-price')[:8]
    )

    # Prepare product info with like status and count
    product_infos = []
    user = request.user if request.user.is_authenticated else None
    for product in popular_products:
        liked = False
        if user:
            liked = product.likes.filter(user=user).exists()
        like_count = product.likes.count()
        product_infos.append({
            'product': product,
            'liked': liked,
            'like_count': like_count,
        })

    return render(request, 'home.html', {
        "product_infos": product_infos,
    })
