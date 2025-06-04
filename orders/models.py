from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from decimal import Decimal, ROUND_HALF_UP
import uuid
import random

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
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)      # Последнее обновление

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # 🆕 Статус заказа

    confirmed = models.BooleanField(default=False)

    full_name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    order_number = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4().int)[:8]  # 8-значный номер
        super().save(*args, **kwargs)

    def generate_order_number(self):
        return str(random.randint(10_000_000, 99_999_999))

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def total_with_tax(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        tax_rate = Decimal('0.10')
        tax = total * tax_rate
        final_total = total + tax
        return final_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
