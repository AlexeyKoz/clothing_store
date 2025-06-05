from catalog.models import Product
from decimal import Decimal, ROUND_HALF_UP
import uuid
import random
from django.db import models
from django.contrib.auth.models import User

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name}, {self.address}, {self.city}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmed = models.BooleanField(default=False)

    # 📦 Связь с ShippingAddress
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.SET_NULL)

    # 💳 Поля оплаты
    payment_method = models.CharField(max_length=50, blank=True)
    installments = models.PositiveIntegerField(default=1)
    name_on_bill = models.CharField(max_length=100, blank=True)

    # 📄 Данные для выставления счёта (копируются из shipping_address при создании)
    full_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    order_number = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4().int)[:8]
        super().save(*args, **kwargs)

    def generate_order_number(self):
        return str(random.randint(10_000_000, 99_999_999))

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def subtotal(self):
        return sum(item.price * item.quantity for item in self.items.all())

    def tax(self):
        return (self.subtotal() * Decimal('0.17')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def total_with_tax(self):
        return (self.subtotal() + self.tax()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
