import os
import sys
import django
import random
from django.utils.text import slugify

# Настройка Django для посторонних скриптов
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Product, Brand, Category, Color, Size

# Демо-данные
colors = [
    ("Red", "#FF0000"), ("Blue", "#0000FF"), ("Green", "#00FF00"),
    ("Black", "#000000"), ("White", "#FFFFFF"), ("Yellow", "#FFFF00"), ("Purple", "#800080")
]
sizes = ["XS", "S", "M", "L", "XL"]
categories = {
    'WO': 'Women', 'ME': 'Men', 'KI': 'Kids', 'BO': 'Boys',
    'GI': 'Girls', 'SH': 'Shoes', 'HO': 'Home'
}
brands = [
    "Abidas", "Puima", "Nyke", "Reebak", "Livi’s", "H&N", "Zarra", "Guccy",
    "Kelvin Clain", "Tammy Hilviger", "Under Armore", "Laqoste", "Convurse",
    "New Balenzo", "Kolumbia"
]

# Создаем/находим объекты
# Populate categories
cat_objs = {}
for code, name in categories.items():
    slug = slugify(name)
    category = Category.objects.filter(slug=slug).first()
    if not category:
        category = Category.objects.create(name=name, slug=slug)
    cat_objs[code] = category

brand_objs = {}
for name in brands:
    obj, _ = Brand.objects.get_or_create(name=name)
    brand_objs[name] = obj

color_objs = []
for name, hex_code in colors:
    obj, _ = Color.objects.get_or_create(name=name, hex_code=hex_code)
    color_objs.append(obj)

size_objs = []
for size in sizes:
    obj, _ = Size.objects.get_or_create(name=size)
    size_objs.append(obj)

# Чистим старые демо-товары
Product.objects.all().delete()

# Создаем 100 товаров
for i in range(1, 101):
    cat_code = random.choice(list(categories.keys()))
    category = cat_objs[cat_code]
    brand_name = random.choice(brands)
    brand_obj = brand_objs[brand_name]
    product_name = f"Product {i}"
    price = round(random.uniform(10, 200), 2)
    desc = f"This is a high-quality {category.name.lower()} product."
    rating = random.randint(1, 5)
    review = f"Rated {rating} stars. Very nice item!"
    liked = random.choice([True, False])
    internal_code = f"{cat_code}{random.randint(10,99)}-{random.randint(100,999)}"
    image_path = f"products/{i}.jpg"

    product = Product.objects.create(
        name=product_name,
        description=desc + "\n" + review,
        price=price,
        category=category,
        brand=brand_obj,
        image=image_path,
    )
    product.colors.set(random.sample(color_objs, k=random.randint(1, 3)))
    product.sizes.set(random.sample(size_objs, k=random.randint(1, 2)))

print("100 demo products with images and details added to the database.")
