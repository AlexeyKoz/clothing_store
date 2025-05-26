from django.contrib.auth.models import User
from users.models import UserProfile
import random
import datetime

first_names = ["Alex", "Dana", "Max", "Ella", "Lior", "Maya", "Tom", "Noa", "Ben", "Sophie"]
last_names = ["Levi", "Cohen", "Smith", "Goldberg", "Katz", "Shapiro", "Adler", "Weiss", "Mizrahi", "Green"]

countries_local = ["IL"]
countries_foreign = ["US", "UK", "DE", "FR"]

user_types = ["regular", "vip", "international"]

def random_date_of_birth():
    year = random.randint(1980, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)


# Create 10 regular users (local)
for i in range(10):
    username = f"user{i}"
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@example.com",
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
        }
    )
    if created:
        user.set_password("password123")
        user.save()
        UserProfile.objects.create(
            user=user,
            user_type="regular",
            address="Israel, Tel Aviv",
            date_of_birth=random_date_of_birth(),
            country="IL"
        )

# Create 3 VIP users (local)
for i in range(3):
    username = f"vip_user{i}"
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@vip.com",
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
        }
    )
    if created:
        user.set_password("vip12345")
        user.save()
        UserProfile.objects.create(
            user=user,
            user_type="vip",
            address="Israel, Herzliya",
            date_of_birth=random_date_of_birth(),
            country="IL"
        )

# Create 4 international users
for i in range(4):
    username = f"intl_user{i}"
    country = random.choice(countries_foreign)
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@intl.com",
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
        }
    )
    if created:
        user.set_password("intlpass123")
        user.save()
        UserProfile.objects.create(
            user=user,
            user_type="international",
            address=f"Foreign Address, {country}",
            date_of_birth=random_date_of_birth(),
            country=country
        )

print("Users with profiles created.")
