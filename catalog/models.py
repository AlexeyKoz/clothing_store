from django.db import models
from django.conf import settings

# Category model — e.g. Boys, Girls, Women, etc.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# Brand model — optional, but useful
class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Color model — for filtering by color
class Color(models.Model):
    name = models.CharField(max_length=30)
    hex_code = models.CharField(max_length=7, help_text="Hex code (e.g. #FF0000)")

    def __str__(self):
        return self.name


# Size model — e.g. S, M, L, 38, 40, etc.
class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


# Product model — main item
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relations
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)

    # Media
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class ProductLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_likes",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} likes {self.product}"
