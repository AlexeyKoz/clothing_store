import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Product, ProductLike
from django.contrib.auth import get_user_model
import random

User = get_user_model()

users = User.objects.all()
products = Product.objects.all()

for user in users:
    liked = random.sample(list(products), k=min(5, len(products)))
    for product in liked:
        ProductLike.objects.get_or_create(user=user, product=product)

print("👍 Product likes populated.")
