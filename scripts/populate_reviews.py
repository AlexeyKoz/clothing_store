import django
import os
import sys
import random
from faker import Faker


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Product
from reviews.models import Review
from django.contrib.auth.models import User

fake = Faker()
users = list(User.objects.all())
products = list(Product.objects.all())

for _ in range(100):
    Review.objects.create(
        product=random.choice(products),
        user=random.choice(users),
        rating=random.randint(1, 5),
        comment=fake.paragraph(),
    )

print("Reviews populated.")
