#!/usr/bin/env python
from catalog.models import Product
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


# Count total products
total_products = Product.objects.count()
print(f"Total products in database: {total_products}")

# Count products with likes
products_with_likes = Product.objects.annotate(
    num_likes=django.db.models.Count('likes')).filter(num_likes__gt=0).count()
print(f"Products with likes: {products_with_likes}")

# Show first few products
print("\nFirst 5 products:")
for product in Product.objects.all()[:5]:
    likes = product.likes.count()
    print(f"- {product.name} (Likes: {likes})")
