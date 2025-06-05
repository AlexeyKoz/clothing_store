import os
import django
import random
import sys
from faker import Faker

# Устанавливаем настройки Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from orders.models import ShippingAddress  # Замени путь, если у тебя другой
fake = Faker()

def create_shipping_addresses():
    users = User.objects.all()
    for user in users:

        if ShippingAddress.objects.filter(user=user).exists():
            continue

        ShippingAddress.objects.create(
            user=user,
            full_name=user.get_full_name() or fake.name(),
            address=fake.street_address(),
            city=fake.city(),
            zip_code=fake.postcode(),
            country=fake.country()
        )
        print(f"✅ Address created for {user.username}")

if __name__ == "__main__":
    create_shipping_addresses()
