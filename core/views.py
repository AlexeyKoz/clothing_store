from django.shortcuts import render
from catalog.models import Product, ProductLike
from django.core.cache import cache
from django.db import models
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


def home_view(request):
    # Get page number from request
    page_number = request.GET.get('page', 1)
    products_per_page = 12  # Show 12 products per page

    # Order products by number of likes (popularity), then by price
    popular_products = (
        Product.objects.annotate(num_likes=models.Count('likes'))
        .order_by('-num_likes', '-price')
    )

    # Create paginator
    paginator = Paginator(popular_products, products_per_page)
    page_obj = paginator.get_page(page_number)

    # Prepare product info with like status and count
    product_infos = []
    user = request.user if request.user.is_authenticated else None
    for product in page_obj:
        liked = False
        if user:
            liked = product.likes.filter(user=user).exists()
        like_count = product.likes.count()
        product_infos.append({
            'product': product,
            'liked': liked,
            'like_count': like_count,
        })

    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('core/product_cards.html', {
            'product_infos': product_infos
        }, request=request)
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None
        })

    return render(request, 'home.html', {
        "product_infos": product_infos,
        "has_next": page_obj.has_next(),
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None
    })
