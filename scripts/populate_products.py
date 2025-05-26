import random
from catalog.models import Product, Category, Brand, Color, Size

# Примерный список названий и описаний
names = [
    "Basic T-Shirt", "Classic Hoodie", "Slim Jeans", "Running Shoes", "Summer Dress",
    "Leather Jacket", "Cotton Shorts", "Sweatpants", "Long Sleeve Shirt", "Denim Skirt"
]

descriptions = [
    "High-quality and comfortable.",
    "Perfect for everyday wear.",
    "Made with durable materials.",
    "Best choice for casual style.",
    "Simple, stylish and practical."
]

# Получаем связанные объекты
categories = list(Category.objects.all())
brands = list(Brand.objects.all())
colors = list(Color.objects.all())
sizes = list(Size.objects.all())

# Создаём товары
for i in range(10):
    name = names[i % len(names)]
    product, created = Product.objects.get_or_create(
        name=f"{name} #{i+1}",
        defaults={
            'description': random.choice(descriptions),
            'price': round(random.uniform(10.00, 200.00), 2),
            'category': random.choice(categories),
            'brand': random.choice(brands),
            'in_stock': random.choice([True, True, False])
        }
    )
    if created:
        # Привязка many-to-many полей
        product.colors.set(random.sample(colors, k=min(2, len(colors))))
        product.sizes.set(random.sample(sizes, k=min(3, len(sizes))))
        product.save()

print("10 demo products created.")
